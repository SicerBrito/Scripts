#!/bin/bash

# Cambiar al directorio Documents
cd ~/Documents/

# Crear la estructura de carpetas y archivos
mkdir ProyectoApi
cd ProyectoApi
dotnet new sln
dotnet new classlib -o Dominio
dotnet new classlib -o Persistencia
dotnet new classlib -o Aplicacion
dotnet new webapi -o ApiSicer
dotnet sln add Dominio/
dotnet sln add Aplicacion/
dotnet sln add ApiSicer/

# Crear las referencias
cd Persistencia/
dotnet add reference ../Dominio/
cd ..
cd Aplicacion/
dotnet add reference ../Dominio/
dotnet add reference ../Persistencia/
cd ..
cd ApiSicer/
dotnet add reference ../Aplicacion/
cd ..

# Instalación de herramientas
cd Dominio/
dotnet add package Microsoft.EntityFrameworkCore --version 7.0.10
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection --version 11.1.0
dotnet add package AutoMapper.Extensions.Microsoft.DependencyInjection --version 12.0.1
dotnet add package FluentValidation.AspNetCore --version 11.3.0
dotnet add package itext7.pdfhtml --version 5.0.1
cd ..
cd Persistencia/
dotnet add package Microsoft.EntityFrameworkCore --version 7.0.10
dotnet add package Pomelo.EntityFrameworkCore.MySql --version 7.0.0
dotnet add package Dapper --version 2.0.151
cd ..
cd ApiSicer/
dotnet add package Microsoft.EntityFrameworkCore.Design --version 7.0.10
dotnet add package Newtonsoft.Json --version 13.0.3
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer --version 7.0.10
dotnet add package Swashbuckle.AspNetCore --version 6.5.0
cd ..

# Crear la estructura de los archivos dentro de Dominio
cd Dominio/
mkdir Entities/
cd Entities/
echo 'namespace Dominio.Entities;
    public class BaseEntity{
        
        public int Id { get; set; }
        
    }' > BaseEntity.cs
cd ..

mkdir Interfaces/
cd Interfaces/
echo 'using System.Linq.Expressions;
using Dominio.Entities;

namespace Dominio.Interfaces;
    public interface IGenericRepository<T> where T : BaseEntity{

        Task<T> ? GetByIdAsync(string Id);
        Task<IEnumerable<T>> GetAllAsync();
        IEnumerable<T> Find(Expression<Func<T, bool>> expression);
        void Add(T entity);
        void AddRange(IEnumerable<T> entities);
        void Remove(T entity);
        void RemoveRange(IEnumerable<T> entities);
        void Update(T entity);

    }' > IGenericRepository.cs

echo 'namespace Dominio.Interfaces;
    public interface IUnitOfWork{
        INombreInterfas ? PluralInterfas { get; }
        Task<int> SaveAsync();
    }' > IUnitOfWork.cs
cd ..
cd ..

# Crear la estructura de los archivos dentro de Persistencia
cd Persistencia/
mkdir Data/
cd Data/

echo 'using System.Reflection;
using Dominio.Entities;
using Microsoft.EntityFrameworkCore;

namespace Persistencia.Data;
public class SicerWebApiContext : DbContext{
    public SicerWebApiContext(DbContextOptions<SicerWebApiContext> options) : base(options){

    }

    public DbSet<NombreEntidad> NombreEnPlural { get; set; } = null!;

    protected override void OnModelCreating(ModelBuilder modelBuilder){
        base.OnModelCreating(modelBuilder);
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }
}' > SicerContext.cs

mkdir Configuration/
cd ..

# Crear la estructura de los archivos dentro de Aplicacion
cd Aplicacion/
mkdir Repository/
cd Repository/
echo 'using System.Linq.Expressions;
using Dominio.Entities;
using Dominio.Interfaces;
using Microsoft.EntityFrameworkCore;
using Persistencia.Data;

namespace Aplicacion.Repository;
public class GenericRepository<T> : IGenericRepository<T> where T : BaseEntity
{

    private readonly SicerContext _context;
    
    public GenericRepository(SicerContext context)
    {
        _context = context;
    }
    
    public virtual void Add(T entity)
    {        
        _context.Set<T>().Add(entity);
    }

    public virtual void AddRange(IEnumerable<T> entities)
    {
        _context.Set<T>().AddRange(entities);
    }

    public virtual IEnumerable<T> Find(Expression<Func<T, bool>> expression)
    {
        return  _context.Set<T>().Where(expression);
    }

    public virtual async Task<IEnumerable<T>> GetAllAsync()
    {
        return await _context.Set<T>().ToListAsync();
    }

    public virtual async Task<T>? GetByIdAsync(string Id)
    {
        return (await _context.Set<T>().FindAsync(Id))!;
    }

    public virtual void Remove(T entity)
    {
        _context.Set<T>().Remove(entity);
    }

    public virtual void RemoveRange(IEnumerable<T> entities)
    {
        _context.Set<T>().RemoveRange(entities);
    }

    public virtual void Update(T entity)
    {
        _context.Set<T>().Update(entity);
    }

}' > GenericRepository.cs

cd ..

mkdir UnitOfWork/
cd UnitOfWork/
echo 'using Aplicacion.Repository;
using Dominio.Interfaces;
using Persistencia.Data;

namespace Aplicacion.UnitOfWork;
public class UnitOfWork : IUnitOfWork, IDisposable
{
    private INombreRepository? _NombreSingular;
    private readonly SicerContext _Context;

    public UnitOfWork(SicerContext context)=> _Context = context;
    
    public INombreRepository? NombrePlural => _NombreSingular ??= new NombreRepository(_Context);




    public void Dispose()
    {
        _Context.Dispose();
    }

    public async Task<int> SaveAsync()
    {
        return await _Context.SaveChangesAsync();
    }
}' > UnitOfWork.cs

cd ..
cd ..

# Crear la estructura de los archivos dentro de ApiSicer
cd ApiSicer/
mkdir Extensions/
cd Extensions/
echo 'using Aplicacion.UnitOfWork;
using Dominio.Interfaces;

namespace ApiSicer.Extensions;

    public static class ApplicationServiceExtension{

        public static void ConfigureCors(this IServiceCollection services) =>
            services.AddCors(options => {
                options.AddPolicy("CorsPolicy",builder=>
                    builder.AllowAnyOrigin()        //WithOrigins("http://domini.com")
                    .AllowAnyMethod()               //WithMethods(*GET", "POST")
                    .AllowAnyHeader());             //WithHeaders(*accept*, "content-type")
            });


        public static void AddAplicacionServices(this IServiceCollection services){
            services.AddScoped<IUnitOfWork,UnitOfWork>();
        }

        
    }' > ApplicationServiceExtension.cs

cd ..

echo 'using ApiSicer.Extensions;
using Microsoft.EntityFrameworkCore;
using Persistencia.Data;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
builder.Services.ConfigureCors();
builder.Services.AddAplicacionServices();

builder.Services.AddDbContext<SicerContext>(options =>
{
    string ? connectionString = builder.Configuration.GetConnectionString("ConexMysql");
    options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));
});

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("CorsPolicy");

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();' > Program.cs

mkdir Dtos/
mkdir Profile/
mkdir Helpers/
cd ..
echo "Proyecto configurado exitosamente."

code . && exit

