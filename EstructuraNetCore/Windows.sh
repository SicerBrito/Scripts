#!/bin/bash
cd ..
cd ..

cd Documents

# Función para mostrar el menú y obtener el nombre del archivo
get_file_name() {
    read -p "Ingrese el nombre que va a tener archivo/carpeta: " file_name
}

# Función para crar la carpeta que va contener todo el proyecto
create_project_folder() {
    mkdir "$1" ; cd "$1"
}

# Función para crear una nueva aplicación webapi con dotnet
create_webapi() {
    dotnet new webapi -o Api"$1"
    # Crear la estructura de carpetas y archivos
    dotnet new sln
    dotnet new classlib -o Dominio
    dotnet new classlib -o Persistencia
    dotnet new classlib -o Aplicacion
    dotnet new classlib -o Seguridad
    dotnet sln add Dominio
    dotnet sln add Aplicacion
    dotnet sln add Seguridad 
    dotnet sln add Api"$1" 

    # Crear las referencias
    cd Persistencia 
    dotnet add reference ..\\Dominio\\

    cd .. 
    cd Aplicacion 
    dotnet add reference ..\\Dominio\\ 

    dotnet add reference ..\\Persistencia\\

    cd ..
    cd Seguridad 
    dotnet add reference ..\\Aplicacion\\

    cd ..
    cd Api"$1"  
    dotnet add reference ..\\Aplicacion\\

    dotnet add reference ..\\Seguridad\\

    cd .. 

    # Instalación de herramientas
    cd Dominio 
    dotnet add package Microsoft.EntityFrameworkCore --version 7.0.10
    dotnet add package MediatR.Extensions.Microsoft.DependencyInjection --version 11.1.0
    dotnet add package AutoMapper.Extensions.Microsoft.DependencyInjection --version 12.0.1
    dotnet add package FluentValidation.AspNetCore --version 11.3.0
    dotnet add package itext7.pdfhtml --version 5.0.1
    cd ..
    cd Persistencia 
    dotnet add package Microsoft.EntityFrameworkCore --version 7.0.10
    dotnet add package Pomelo.EntityFrameworkCore.MySql --version 7.0.0
    dotnet add package Dapper --version 2.0.151
    cd ..
    cd Seguridad
    dotnet add package System.IdentityModel.Tokens.Jwt --version 6.32.2
    cd ..
    cd Api"$1"
    dotnet add package Microsoft.EntityFrameworkCore.Design --version 7.0.10
    dotnet add package Newtonsoft.Json --version 13.0.3
    dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer --version 7.0.10
    dotnet add package Swashbuckle.AspNetCore --version 6.5.0
    cd ..

# Crear la estructura de los archivos dentro de Dominio
cd Dominio
mkdir Entities 
cd Entities
echo 'namespace Dominio.Entities;
    public class BaseEntity{
        
        public int Id { get; set; }
        
    }' > BaseEntity.cs

echo 'namespace Dominio.Entities;
    public class BaseEntityA{
        
        public string ? Id { get; set; }
        
    }' > BaseEntityA.cs

cd ..

mkdir Interfaces 
cd Interfaces
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

# Crear la estructura de los archivos dentro de Aplicacion
cd Aplicacion
mkdir Repository
cd Repository
echo 'using System.Linq.Expressions;
using Dominio.Entities;
using Dominio.Interfaces;
using Microsoft.EntityFrameworkCore;
using Persistencia.Data;

namespace Aplicacion.Repository;
public class GenericRepository<T> : IGenericRepository<T> where T : BaseEntity
{

    private readonly NameContext _context;
    
    public GenericRepository(NameContext context)
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

mkdir UnitOfWork  
cd UnitOfWork 
echo 'using Aplicacion.Repository;
using Dominio.Interfaces;
using Persistencia.Data;

namespace Aplicacion.UnitOfWork;
public class UnitOfWork : IUnitOfWork, IDisposable
{
    private INombreRepository? _NombreSingular;
    private readonly NameContext _Context;

    public UnitOfWork(NameContext context)=> _Context = context;
    
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

mkdir Contratos
cd Contratos
echo 'using Dominio.Entities;

namespace Aplicacion.Contratos;
    public interface IJwtGenerator{
        string  CrearTopken(Pais pais);
    }' > IJwtGenerator.cs
    
cd ..
cd ..

cd Seguridad
mkdir TokenSeguridad
cd TokenSeguridad

echo 'using System.Security.Claims;
using Aplicacion.Contratos;
using Dominio.Entities;

namespace Seguridad.TokenSeguridad;
public class JwtGenerador : IJwtGenerator
{
    public string CrearTopken(Pais pais)
    {
        var claims = new List<Claim>{
            
        };
    }
}' > JwtGenerador.cs

cd ..
cd ..

# Crear la estructura de los archivos dentro de la carpeta Api
cd Api"$1"  
cd Controllers  
echo "using Microsoft.AspNetCore.Mvc;

namespace Api"$1".Controllers;

[ApiController]
[Route("api/sicer[controller]")]

public class ApiBaseController : ControllerBase
{
    
}" > ApiBaseController.cs
cd ..

mkdir Extensions 
cd Extensions 
echo "using Aplicacion.UnitOfWork;
using Dominio.Interfaces;

namespace Api"$1".Extensions;

    public static class ApplicationServiceExtension{

        public static void ConfigureCors(this IServiceCollection services) =>
            services.AddCors(options => {
                options.AddPolicy("CorsPolicy",builder=>
                    builder.AllowAnyOrigin()        //WithOrigins("http://domini.com")
                    .AllowAnyMethod()               //WithMethods(*GET*, "POST")
                    .AllowAnyHeader());             //WithHeaders(*accept*, "content-type")
            });


        public static void AddAplicacionServices(this IServiceCollection services){
            services.AddScoped<IUnitOfWork,UnitOfWork>();
        }

        
    }" > ApplicationServiceExtension.cs

cd ..

echo "using Api"$1".Extensions;
using Microsoft.EntityFrameworkCore;
using Persistencia.Data;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
builder.Services.ConfigureCors();
builder.Services.AddAplicacionServices();

builder.Services.AddDbContext<NameContext>(options =>
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

app.Run();" > Program.cs

echo '{
  "ConnectionStrings": {
    "ConexSqlServer": "Data Source=localhost\\sqlexpress;Initial Catalog=dB;Integrate Security=True",
    "ConexMysql": "server=localhost;user=root;password=123456;database=sicerprobando"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}' > appsettings.Development.json

echo '{
  "ConnectionStrings": {
    "ConexSqlServer": "Data Source=localhost\\sqlexpress;Initial Catalog=dB;Integrate Security=True",
    "ConexMysql": "server=localhost;user=root;password=123456;database=sicerdatabase"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "JWT" : {
    "Key" : "rgfZs3pNboV0hbg6Fat46Xtaw2GGBABY",
    "Issuer" : "WebApi",
    "Audience" : "WebApi",
    "DurationInMinutes" : 20
  }
}' > appsettings.json

mkdir Dtos  
mkdir Profile  
cd Profile 
echo "using AutoMapper;
using Dominio.Entities;
using Api"$1".Dtos;


namespace Api"$1".Profiles;
    public class MappingProfiles : Profile{

        public MappingProfiles(){
            CreateMap<Alumno, AlumnoDto>()
                .ReverseMap();

            /* .ForMember(p => p.Profesores) */
        }
    }" > MappingProfiles.cs
cd ..

cd Properties
echo '{
  "$schema": "https://json.schemastore.org/launchsettings.json",
  "iisSettings": {
    "windowsAuthentication": false,
    "anonymousAuthentication": true,
    "iisExpress": {
      "applicationUrl": "http://localhost:56880",
      "sslPort": 44381
    }
  },
  "profiles": {
    "http": {
      "commandName": "Project",
      "dotnetRunMessages": true,
      "launchBrowser": true,
      "launchUrl": "swagger",
      "applicationUrl": "http://localhost:5000",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    },
    "https": {
      "commandName": "Project",
      "dotnetRunMessages": true,
      "launchBrowser": true,
      "launchUrl": "swagger",
      "applicationUrl": "https://localhost:5001;http://localhost:5000",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    },
    "IIS Express": {
      "commandName": "IISExpress",
      "launchBrowser": true,
      "launchUrl": "swagger",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    }
  }
}' > launchSettings.json

cd ..
mkdir Helpers
cd ..

echo "Se ha creado toda la estructura base del proyecto"

}

# Función para crear una nueva entidad
create_entity() {
    
cd Dominio 
cd Entities  

echo "namespace Dominio.Entities;
public class "$1" : BaseEntity{

    public ICollection<Profesor> ? Profesores { get; set; } = new HashSet<Profesor>();
    public ICollection<Salon> ? Salones { get; set;}
}" > "$1".cs
cd ..
cd ..
}

# Función para crear un nuevo archivo context
create_context() {
cd Persistencia  
mkdir Data 
cd Data

context_name="$1"Context  # Almacena el nombre del contexto

echo "using System.Reflection;
using Dominio.Entities;
using Microsoft.EntityFrameworkCore;

namespace Persistencia.Data;
public class $context_name : DbContext{
    public $context_name(DbContextOptions<$context_name> options) : base(options){

    }

    public DbSet<NombreEntidad> NombreEnPlural { get; set; } = null!;

    protected override void OnModelCreating(ModelBuilder modelBuilder){
        base.OnModelCreating(modelBuilder);
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }
}" > "$context_name".cs

mkdir Configuration 
cd ..
cd ..
}

# Función para crear un nuevo archivo de configuración
create_configuración() {

cd Persistencia
cd Data
cd Configuration

config_name="$1"Configuration  # Almacena el nombre de la configuración

echo "using Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Persistencia.Data.Configuration;
public class "$file_name" : IEntityTypeConfiguration<{"$file_name"}>
{
    public void Configure(EntityTypeBuilder<{"$file_name"}> builder)
    {
        builder.ToTable("{"$file_name"}");

        builder.Property(p => p.)
            .HasAnnotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn)
            .HasColumnName("")
            .HasColumnType("")
            .IsRequired();

        builder.Property(p => p.)
            .HasColumnName("")
            .HasColumnType("")
            .HasMaxLength()
            .IsRequired();

        builder.HasOne(p => p.)
            .WithMany(p => p.)
            .HasForeignKey(p => p.);

        builder.HasMany(p => p.)
            .WithMany(p => p.)
            .UsingEntity<>(
                p => p
                    .HasOne(p => p.)
                    .WithMany(p => p.)
                    .HasForeignKey(p => p.),
                p => p
                    .HasOne(p => p.)
                    .WithMany(p => p.)
                    .HasForeignKey(p => p.),
                p => {
                    p.HasKey(p=> new {p.,p.});                    
                }
            );
    }
}" > "$file_name".cs

cd ..
cd ..
cd ..

}

create_interface() {
cd Dominio
cd Interfaces

mkdir "$1"

interface_name="$1"Repository # Almacena el nombre de la interface

echo "using Dominio.Entities;

namespace Dominio.Interfaces;
    public interface "$interface_name" : IGenericRepository<"$1">{
        
    }" > "$interface_name".cs

cd ..
cd ..
}

create_repository() {
cd Aplicacion
cd Repository

repository_name="$1"Repository # Almacena el nombre del repositorio

echo "using Dominio.Entities;
using Dominio.Interfaces;
using Persistencia.Data;
using Microsoft.EntityFrameworkCore;
namespace Aplicacion.Repository;
public class $repository_name : GenericRepository<Alumno>, I$repository_name
{
    private readonly NameContext _Context;
    public AlumnoRepository(NameContext context) : base(context)
    {
        _Context = context;
    }


    public override async Task<IEnumerable<Alumno>> GetAllAsync()
    {
        return await _Context.Alumnos
            .Include(p => (p.Profesores as List<Profesor>).Select(i=>i.Nombre)) //Si no se coloca en la parte del json apareceria como null            
            .ToListAsync();
    }

}" > $repository_name.cs

mkdir Configuration 
cd .. 
cd .. 
}

# Main
while true; do
    clear
    echo "-------------------------------- Menu Proyecto --------------------------------"
    echo "Recuerde comenzar el nombre de los archivos o carpetas con la primera letra en Mayúscula"
    echo "1. Crear la carpeta del Proyecto"
    echo "2. Crear la aplicación WebApi junto al resto de la estructura"
    echo "3. Crear el archivo context dentro de la carpeta Data"
    echo "4. Crear los archivos Entidades dentro de la carpeta Dominio"
    echo "5. Crear los archivos Configuraciones dentro de la carpeta Persistencia/Data/Configurations"
    echo "6. Crear los archivos Interfaces dentro de la carpeta Dominio/Interfaces"
    echo "7. Crear los archivos Repositorios dentro de la carpeta Aplicacion/Repository"
    echo "8. Crear los archivos Dtos dentro de la carpeta WebApi"
    echo "9. Crear los archivos Controllers dentro de la carpeta WebApi"
    echo "10. Salir"
    read -p "Seleccione una opción: " choice

    case $choice in
        1)  # Carpeta del proyecto
            get_file_name
            create_project_folder "$file_name"
            echo "Se ha creado la carpeta $file_name"
            ;;

        2)  # Estructura base y WebApi
            get_file_name
            create_webapi "$file_name"
            ;;

        3)  # Archivo context y las carpetas Data y Configuration
            get_file_name
            create_context "$file_name"
            echo "Se ha creado el archivo "$file_name"Context"
            ;;

        4)  # Crear Entidad dentro de Dominio/Entities
            get_file_name
            create_entity
            echo "Se ha creado la entidad $file_name"
            ;;

        5)  # Crear Canfiguracion dentro de Data/Configuration
            get_file_name
            create_configuración
            echo "Se ha creado el archivo "$file_name"Configuración"
            ;;

        6)  # Crear Interfas dentro de Dominio/Interfaces
            get_file_name
            create_interface
            echo "Se ha creado el archivo I$file_name"
            ;;

        7)  # Crear Repositorio dentro de la carpeta Aplicacion/Repository
            get_file_name
            create_repository
            echo "Se ha creado el archivo $file_name"
            ;;

        8)  # Crear Dto dentro de la carpeta WebApi/Dtos
            get_file_name
            ;;

        9)  # Crear Controller dentro de la carpeta WebApi/Controllers
            get_file_name
            ;;

        10)  # Salir del Menu
            echo "Saliendo..."
            break
            ;;
        *)
            echo "Opción no válida"
            clear
            ;;
    esac

    read -p "Presione Enter para continuar..."

done