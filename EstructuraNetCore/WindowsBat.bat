@echo off
cd ..
cd ..

cd Documents

:: Función para obtener el nombre del archivo/carpeta
:get_file_name
set /p file_name="Ingrese el nombre que va a tener archivo/carpeta: "

:: Función para crear la carpeta que va a contener todo el proyecto
:create_project_folder
mkdir "%file_name%" 
cd "%file_name%"
goto :EOF

:: Función para crear una nueva aplicación webapi con dotnet
:create_webapi
dotnet new webapi -o Api%file_name%
:: Crear la estructura de carpetas y archivos
dotnet new sln
dotnet new classlib -o Dominio
dotnet new classlib -o Persistencia
dotnet new classlib -o Aplicacion
dotnet new classlib -o Seguridad
dotnet sln add Dominio
dotnet sln add Aplicacion
dotnet sln add Seguridad 
dotnet sln add Api%file_name%

:: Crear las referencias
cd Persistencia 
dotnet add reference ..\Dominio\

cd .. 
cd Aplicacion 
dotnet add reference ..\Dominio\ 
dotnet add reference ..\Persistencia\

cd ..
cd Seguridad 
dotnet add reference ..\Aplicacion\

cd ..
cd Api%file_name%
dotnet add reference ..\Aplicacion\
dotnet add reference ..\Seguridad\

cd .. 

:: Instalación de herramientas
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
cd Api%file_name%
dotnet add package Microsoft.EntityFrameworkCore.Design --version 7.0.10
dotnet add package Newtonsoft.Json --version 13.0.3
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer --version 7.0.10
dotnet add package Swashbuckle.AspNetCore --version 6.5.0
cd ..

:: Crear la estructura de los archivos dentro de Dominio
cd Dominio
mkdir Entities 
cd Entities
echo using Dominio.Entities;^
    public class BaseEntity{^
        public int Id { get; set; }^
    } > BaseEntity.cs

echo using Dominio.Entities;^
    public class BaseEntityA{^
        public string ? Id { get; set; }^
    } > BaseEntityA.cs

cd ..

mkdir Interfaces 
cd Interfaces
echo using System.Linq.Expressions;^
using Dominio.Entities;^
^
namespace Dominio.Interfaces;^
    public interface IGenericRepository<T> where T : BaseEntity{^
^
        Task<T> ? GetByIdAsync(string Id);^
        Task<IEnumerable<T>> GetAllAsync();^
        IEnumerable<T> Find(Expression<Func<T, bool>> expression);^
        void Add(T entity);^
        void AddRange(IEnumerable<T> entities);^
        void Remove(T entity);^
        void RemoveRange(IEnumerable<T> entities);^
        void Update(T entity);^
^
    } > IGenericRepository.cs

echo using Dominio.Interfaces;^
    public interface IUnitOfWork{^
        INombreInterfas ? PluralInterfas { get; }^
        Task<int> SaveAsync();^
    } > IUnitOfWork.cs
cd ..
cd ..

:: Crear la estructura de los archivos dentro de Aplicacion
cd Aplicacion
mkdir Repository
cd Repository
echo using Dominio.Entities;^
using Dominio.Interfaces;^
using Persistencia.Data;^
using Microsoft.EntityFrameworkCore;^
^
namespace Aplicacion.Repository;^
public class GenericRepository<T> : IGenericRepository<T> where T : BaseEntity^
{^
    private readonly NameContext _context;^
    ^
    public GenericRepository(NameContext context)^
    {^
        _context = context;^
    }^
    ^
    public virtual void Add(T entity)^
    {^
        _context.Set<T>().Add(entity);^
    }^
    ^
    public virtual void AddRange(IEnumerable<T> entities)^
    {^
        _context.Set<T>().AddRange(entities);^
    }^
    ^
    public virtual IEnumerable<T> Find(Expression<Func<T, bool>> expression)^
    {^
        return  _context.Set<T>().Where(expression);^
    }^
    ^
    public virtual async Task<IEnumerable<T>> GetAllAsync()^
    {^
        return await _context.Set<T>().ToListAsync();^
    }^
    ^
    public virtual async Task<T>? GetByIdAsync(string Id)^
    {^
        return (await _context.Set<T>().FindAsync(Id))!;^
    }^
    ^
    public virtual void Remove(T entity)^
    {^
        _context.Set<T>().Remove(entity);^
    }^
    ^
    public virtual void RemoveRange(IEnumerable<T> entities)^
    {^
        _context.Set<T>().RemoveRange(entities);^
    }^
    ^
    public virtual void Update(T entity)^
    {^
        _context.Set<T>().Update(entity);^
    }^
} > GenericRepository.cs

cd .. 
cd .. 
cd ..

mkdir UnitOfWork  
cd UnitOfWork 
echo using Aplicacion.Repository;^
using Dominio.Interfaces;^
using Persistencia.Data;^
^
namespace Aplicacion.UnitOfWork;^
public class UnitOfWork : IUnitOfWork, IDisposable^
{^
    private INombreRepository? _NombreSingular;^
    private readonly NameContext _Context;^
    ^
    public UnitOfWork(NameContext context)=> _Context = context;^
    ^
    public INombreRepository? NombrePlural => _NombreSingular ??= new NombreRepository(_Context);^
    ^
    ^
    public void Dispose()^
    {^
        _Context.Dispose();^
    }^
    ^
    public async Task<int> SaveAsync()^
    {^
        return await _Context.SaveChangesAsync();^
    }^
} > UnitOfWork.cs

cd ..

mkdir Contratos
cd Contratos
echo using Dominio.Entities;^
^
namespace Aplicacion.Contratos;^
    public interface IJwtGenerator{^
        string  CrearTopken(Pais pais);^
    } > IJwtGenerator.cs
    
cd ..
cd ..

cd Seguridad
mkdir TokenSeguridad
cd TokenSeguridad

echo using System.Security.Claims;^
using Aplicacion.Contratos;^
using Dominio.Entities;^
^
namespace Seguridad.TokenSeguridad;^
public class JwtGenerador : IJwtGenerator^
{^
    public string CrearTopken(Pais pais)^
    {^
        var claims = new List<Claim>{^
        ^
        };^
    }^
} > JwtGenerador.cs

cd ..
cd ..

:: Crear la estructura de los archivos dentro de la carpeta Api
cd Api%file_name%  
cd Controllers  
echo using Microsoft.AspNetCore.Mvc;^
^
namespace Api%file_name%.Controllers;^
^
[ApiController]^
[Route("api/sicer[controller]")]^
^
public class ApiBaseController : ControllerBase^
{^
    ^
} > ApiBaseController.cs
cd ..

mkdir Extensions 
cd Extensions 
echo using Aplicacion.UnitOfWork;^
using Dominio.Interfaces;^
^
namespace Api%file_name%.Extensions;^
^
    public static class ApplicationServiceExtension{^
^
        public static void ConfigureCors(this IServiceCollection services) =>^
            services.AddCors(options => {^
                options.AddPolicy("CorsPolicy",builder=>^
                    builder.AllowAnyOrigin()        //WithOrigins("http://domini.com")^
                    .AllowAnyMethod()               //WithMethods(GET, "POST")^
                    .AllowAnyHeader());             //WithHeaders(accept, "content-type")^
            });^
^
^
        public static void AddAplicacionServices(this IServiceCollection services)^
        {^
            services.AddScoped<IUnitOfWork,UnitOfWork>();^
        }^
^
    } > ApplicationServiceExtension.cs

cd ..

echo using Api%file_name%.Extensions;^
using Microsoft.EntityFrameworkCore;^
using Persistencia.Data;^
^
var builder = WebApplication.CreateBuilder(args);^
^
// Add services to the container.^
^
builder.Services.AddControllers();^
builder.Services.ConfigureCors();^
builder.Services.AddAplicacionServices();^
^
builder.Services.AddDbContext<NameContext>(options =>^
{^
    string ? connectionString = builder.Configuration.GetConnectionString("ConexMysql");^
    options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));^
});^
^
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle^
builder.Services.AddEndpointsApiExplorer();^
builder.Services.AddSwaggerGen();^
^
var app = builder.Build();^
^
// Configure the HTTP request pipeline.^
if (app.Environment.IsDevelopment())^
{^
    app.UseSwagger();^
    app.UseSwaggerUI();^
}^
^
app.UseCors("CorsPolicy");^
^
app.UseHttpsRedirection();^
^
app.UseAuthorization();^
^
app.MapControllers();^
^
app.Run();^
> Program.cs

echo {^
  "ConnectionStrings": {^
    "ConexSqlServer": "Data Source=localhost\\sqlexpress;Initial Catalog=dB;Integrate Security=True",^
    "ConexMysql": "server=localhost;user=root;password=123456;database=sicerprobando"^
  },^
  "Logging": {^
    "LogLevel": {^
      "Default": "Information",^
      "Microsoft.AspNetCore": "Warning"^
    }^
  }^
} > appsettings.Development.json

echo {^
  "ConnectionStrings": {^
    "ConexSqlServer": "Data Source=localhost\\sqlexpress;Initial Catalog=dB;Integrate Security=True",^
    "ConexMysql": "server=localhost;user=root;password=123456;database=sicerdatabase"^
  },^
  "Logging": {^
    "LogLevel": {^
      "Default": "Information",^
      "Microsoft.AspNetCore": "Warning"^
    }^
  },^
  "AllowedHosts": "*",^
  "JWT" : {^
    "Key" : "rgfZs3pNboV0hbg6Fat46Xtaw2GGBABY",^
    "Issuer" : "WebApi",^
    "Audience" : "WebApi",^
    "DurationInMinutes" : 20^
  }^
} > appsettings.json

mkdir Dtos  
mkdir Profile  
cd Profile 
echo using AutoMapper;^
using Dominio.Entities;^
using Api%file_name%.Dtos;^
^
namespace Api%file_name%.Profiles;^
    public class MappingProfiles : Profile{^
^
        public MappingProfiles(){^
            CreateMap<Alumno, AlumnoDto>()^
                .ReverseMap();^
^
            /* .ForMember(p => p.Profesores) */^
        }^
    } > MappingProfiles.cs
cd ..

cd Properties
echo {^
  "$schema": "https://json.schemastore.org/launchsettings.json",^
  "iisSettings": {^
    "windowsAuthentication": false,^
    "anonymousAuthentication": true,^
    "iisExpress": {^
      "applicationUrl": "http://localhost:56880",^
      "sslPort": 44381^
    }^
  },^
  "profiles": {^
    "http": {^
      "commandName": "Project",^
      "dotnetRunMessages": true,^
      "launchBrowser": true,^
      "launchUrl": "swagger",^
      "applicationUrl": "http://localhost:5000",^
      "environmentVariables": {^
        "ASPNETCORE_ENVIRONMENT": "Development"^
      }^
    },^
    "https": {^
      "commandName": "Project",^
      "dotnetRunMessages": true,^
      "launchBrowser": true,^
      "launchUrl": "swagger",^
      "applicationUrl": "https://localhost:5001;http://localhost:5000",^
      "environmentVariables": {^
        "ASPNETCORE_ENVIRONMENT": "Development"^
      }^
    },^
    "IIS Express": {^
      "commandName": "IISExpress",^
      "launchBrowser": true,^
      "launchUrl": "swagger",^
      "environmentVariables": {^
        "ASPNETCORE_ENVIRONMENT": "Development"^
      }^
    }^
  }^
} > launchSettings.json

cd ..
mkdir Helpers
cd ..

echo "Se ha creado toda la estructura base del proyecto"
