@REM Este script no funciona como deberia

@REM @echo off
@REM cd ..
@REM cd ..

@REM cd Documents

@REM :: Función para obtener el nombre del archivo/carpeta
@REM :get_file_name
@REM set /p file_name="Ingrese el nombre que va a tener archivo/carpeta: "

@REM :: Función para crear la carpeta que va a contener todo el proyecto
@REM :create_project_folder
@REM mkdir "%file_name%" 
@REM cd "%file_name%"
@REM goto :EOF

@REM :: Función para crear una nueva aplicación webapi con dotnet
@REM :create_webapi
@REM dotnet new webapi -o Api%file_name%
@REM :: Crear la estructura de carpetas y archivos
@REM dotnet new sln
@REM dotnet new classlib -o Dominio
@REM dotnet new classlib -o Persistencia
@REM dotnet new classlib -o Aplicacion
@REM dotnet new classlib -o Seguridad
@REM dotnet sln add Dominio
@REM dotnet sln add Aplicacion
@REM dotnet sln add Seguridad 
@REM dotnet sln add Api%file_name%

@REM :: Crear las referencias
@REM cd Persistencia 
@REM dotnet add reference ..\Dominio\

@REM cd .. 
@REM cd Aplicacion 
@REM dotnet add reference ..\Dominio\ 
@REM dotnet add reference ..\Persistencia\

@REM cd ..
@REM cd Seguridad 
@REM dotnet add reference ..\Aplicacion\

@REM cd ..
@REM cd Api%file_name%
@REM dotnet add reference ..\Aplicacion\
@REM dotnet add reference ..\Seguridad\

@REM cd .. 

@REM :: Instalación de herramientas
@REM cd Dominio 
@REM dotnet add package Microsoft.EntityFrameworkCore --version 7.0.10
@REM dotnet add package MediatR.Extensions.Microsoft.DependencyInjection --version 11.1.0
@REM dotnet add package AutoMapper.Extensions.Microsoft.DependencyInjection --version 12.0.1
@REM dotnet add package FluentValidation.AspNetCore --version 11.3.0
@REM dotnet add package itext7.pdfhtml --version 5.0.1
@REM cd ..
@REM cd Persistencia 
@REM dotnet add package Microsoft.EntityFrameworkCore --version 7.0.10
@REM dotnet add package Pomelo.EntityFrameworkCore.MySql --version 7.0.0
@REM dotnet add package Dapper --version 2.0.151
@REM cd ..
@REM cd Seguridad
@REM dotnet add package System.IdentityModel.Tokens.Jwt --version 6.32.2
@REM cd ..
@REM cd Api%file_name%
@REM dotnet add package Microsoft.EntityFrameworkCore.Design --version 7.0.10
@REM dotnet add package Newtonsoft.Json --version 13.0.3
@REM dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer --version 7.0.10
@REM dotnet add package Swashbuckle.AspNetCore --version 6.5.0
@REM cd ..

@REM :: Crear la estructura de los archivos dentro de Dominio
@REM cd Dominio
@REM mkdir Entities 
@REM cd Entities
@REM echo using Dominio.Entities;^
@REM     public class BaseEntity{^
@REM         public int Id { get; set; }^
@REM     } > BaseEntity.cs

@REM echo using Dominio.Entities;^
@REM     public class BaseEntityA{^
@REM         public string ? Id { get; set; }^
@REM     } > BaseEntityA.cs

@REM cd ..

@REM mkdir Interfaces 
@REM cd Interfaces
@REM echo using System.Linq.Expressions;^
@REM using Dominio.Entities;^
@REM ^
@REM namespace Dominio.Interfaces;^
@REM     public interface IGenericRepository<T> where T : BaseEntity{^
@REM ^
@REM         Task<T> ? GetByIdAsync(string Id);^
@REM         Task<IEnumerable<T>> GetAllAsync();^
@REM         IEnumerable<T> Find(Expression<Func<T, bool>> expression);^
@REM         void Add(T entity);^
@REM         void AddRange(IEnumerable<T> entities);^
@REM         void Remove(T entity);^
@REM         void RemoveRange(IEnumerable<T> entities);^
@REM         void Update(T entity);^
@REM ^
@REM     } > IGenericRepository.cs

@REM echo using Dominio.Interfaces;^
@REM     public interface IUnitOfWork{^
@REM         INombreInterfas ? PluralInterfas { get; }^
@REM         Task<int> SaveAsync();^
@REM     } > IUnitOfWork.cs
@REM cd ..
@REM cd ..

@REM :: Crear la estructura de los archivos dentro de Aplicacion
@REM cd Aplicacion
@REM mkdir Repository
@REM cd Repository
@REM echo using Dominio.Entities;^
@REM using Dominio.Interfaces;^
@REM using Persistencia.Data;^
@REM using Microsoft.EntityFrameworkCore;^
@REM ^
@REM namespace Aplicacion.Repository;^
@REM public class GenericRepository<T> : IGenericRepository<T> where T : BaseEntity^
@REM {^
@REM     private readonly NameContext _context;^
@REM     ^
@REM     public GenericRepository(NameContext context)^
@REM     {^
@REM         _context = context;^
@REM     }^
@REM     ^
@REM     public virtual void Add(T entity)^
@REM     {^
@REM         _context.Set<T>().Add(entity);^
@REM     }^
@REM     ^
@REM     public virtual void AddRange(IEnumerable<T> entities)^
@REM     {^
@REM         _context.Set<T>().AddRange(entities);^
@REM     }^
@REM     ^
@REM     public virtual IEnumerable<T> Find(Expression<Func<T, bool>> expression)^
@REM     {^
@REM         return  _context.Set<T>().Where(expression);^
@REM     }^
@REM     ^
@REM     public virtual async Task<IEnumerable<T>> GetAllAsync()^
@REM     {^
@REM         return await _context.Set<T>().ToListAsync();^
@REM     }^
@REM     ^
@REM     public virtual async Task<T>? GetByIdAsync(string Id)^
@REM     {^
@REM         return (await _context.Set<T>().FindAsync(Id))!;^
@REM     }^
@REM     ^
@REM     public virtual void Remove(T entity)^
@REM     {^
@REM         _context.Set<T>().Remove(entity);^
@REM     }^
@REM     ^
@REM     public virtual void RemoveRange(IEnumerable<T> entities)^
@REM     {^
@REM         _context.Set<T>().RemoveRange(entities);^
@REM     }^
@REM     ^
@REM     public virtual void Update(T entity)^
@REM     {^
@REM         _context.Set<T>().Update(entity);^
@REM     }^
@REM } > GenericRepository.cs

@REM cd .. 
@REM cd .. 
@REM cd ..

@REM mkdir UnitOfWork  
@REM cd UnitOfWork 
@REM echo using Aplicacion.Repository;^
@REM using Dominio.Interfaces;^
@REM using Persistencia.Data;^
@REM ^
@REM namespace Aplicacion.UnitOfWork;^
@REM public class UnitOfWork : IUnitOfWork, IDisposable^
@REM {^
@REM     private INombreRepository? _NombreSingular;^
@REM     private readonly NameContext _Context;^
@REM     ^
@REM     public UnitOfWork(NameContext context)=> _Context = context;^
@REM     ^
@REM     public INombreRepository? NombrePlural => _NombreSingular ??= new NombreRepository(_Context);^
@REM     ^
@REM     ^
@REM     public void Dispose()^
@REM     {^
@REM         _Context.Dispose();^
@REM     }^
@REM     ^
@REM     public async Task<int> SaveAsync()^
@REM     {^
@REM         return await _Context.SaveChangesAsync();^
@REM     }^
@REM } > UnitOfWork.cs

@REM cd ..

@REM mkdir Contratos
@REM cd Contratos
@REM echo using Dominio.Entities;^
@REM ^
@REM namespace Aplicacion.Contratos;^
@REM     public interface IJwtGenerator{^
@REM         string  CrearTopken(Pais pais);^
@REM     } > IJwtGenerator.cs
    
@REM cd ..
@REM cd ..

@REM cd Seguridad
@REM mkdir TokenSeguridad
@REM cd TokenSeguridad

@REM echo using System.Security.Claims;^
@REM using Aplicacion.Contratos;^
@REM using Dominio.Entities;^
@REM ^
@REM namespace Seguridad.TokenSeguridad;^
@REM public class JwtGenerador : IJwtGenerator^
@REM {^
@REM     public string CrearTopken(Pais pais)^
@REM     {^
@REM         var claims = new List<Claim>{^
@REM         ^
@REM         };^
@REM     }^
@REM } > JwtGenerador.cs

@REM cd ..
@REM cd ..

@REM :: Crear la estructura de los archivos dentro de la carpeta Api
@REM cd Api%file_name%  
@REM cd Controllers  
@REM echo using Microsoft.AspNetCore.Mvc;^
@REM ^
@REM namespace Api%file_name%.Controllers;^
@REM ^
@REM [ApiController]^
@REM [Route("api/sicer[controller]")]^
@REM ^
@REM public class ApiBaseController : ControllerBase^
@REM {^
@REM     ^
@REM } > ApiBaseController.cs
@REM cd ..

@REM mkdir Extensions 
@REM cd Extensions 
@REM echo using Aplicacion.UnitOfWork;^
@REM using Dominio.Interfaces;^
@REM ^
@REM namespace Api%file_name%.Extensions;^
@REM ^
@REM     public static class ApplicationServiceExtension{^
@REM ^
@REM         public static void ConfigureCors(this IServiceCollection services) =>^
@REM             services.AddCors(options => {^
@REM                 options.AddPolicy("CorsPolicy",builder=>^
@REM                     builder.AllowAnyOrigin()        //WithOrigins("http://domini.com")^
@REM                     .AllowAnyMethod()               //WithMethods(GET, "POST")^
@REM                     .AllowAnyHeader());             //WithHeaders(accept, "content-type")^
@REM             });^
@REM ^
@REM ^
@REM         public static void AddAplicacionServices(this IServiceCollection services)^
@REM         {^
@REM             services.AddScoped<IUnitOfWork,UnitOfWork>();^
@REM         }^
@REM ^
@REM     } > ApplicationServiceExtension.cs

@REM cd ..

@REM echo using Api%file_name%.Extensions;^
@REM using Microsoft.EntityFrameworkCore;^
@REM using Persistencia.Data;^
@REM ^
@REM var builder = WebApplication.CreateBuilder(args);^
@REM ^
@REM // Add services to the container.^
@REM ^
@REM builder.Services.AddControllers();^
@REM builder.Services.ConfigureCors();^
@REM builder.Services.AddAplicacionServices();^
@REM ^
@REM builder.Services.AddDbContext<NameContext>(options =>^
@REM {^
@REM     string ? connectionString = builder.Configuration.GetConnectionString("ConexMysql");^
@REM     options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));^
@REM });^
@REM ^
@REM // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle^
@REM builder.Services.AddEndpointsApiExplorer();^
@REM builder.Services.AddSwaggerGen();^
@REM ^
@REM var app = builder.Build();^
@REM ^
@REM // Configure the HTTP request pipeline.^
@REM if (app.Environment.IsDevelopment())^
@REM {^
@REM     app.UseSwagger();^
@REM     app.UseSwaggerUI();^
@REM }^
@REM ^
@REM app.UseCors("CorsPolicy");^
@REM ^
@REM app.UseHttpsRedirection();^
@REM ^
@REM app.UseAuthorization();^
@REM ^
@REM app.MapControllers();^
@REM ^
@REM app.Run();^
@REM > Program.cs

@REM echo {^
@REM   "ConnectionStrings": {^
@REM     "ConexSqlServer": "Data Source=localhost\\sqlexpress;Initial Catalog=dB;Integrate Security=True",^
@REM     "ConexMysql": "server=localhost;user=root;password=123456;database=sicerprobando"^
@REM   },^
@REM   "Logging": {^
@REM     "LogLevel": {^
@REM       "Default": "Information",^
@REM       "Microsoft.AspNetCore": "Warning"^
@REM     }^
@REM   }^
@REM } > appsettings.Development.json

@REM echo {^
@REM   "ConnectionStrings": {^
@REM     "ConexSqlServer": "Data Source=localhost\\sqlexpress;Initial Catalog=dB;Integrate Security=True",^
@REM     "ConexMysql": "server=localhost;user=root;password=123456;database=sicerdatabase"^
@REM   },^
@REM   "Logging": {^
@REM     "LogLevel": {^
@REM       "Default": "Information",^
@REM       "Microsoft.AspNetCore": "Warning"^
@REM     }^
@REM   },^
@REM   "AllowedHosts": "*",^
@REM   "JWT" : {^
@REM     "Key" : "rgfZs3pNboV0hbg6Fat46Xtaw2GGBABY",^
@REM     "Issuer" : "WebApi",^
@REM     "Audience" : "WebApi",^
@REM     "DurationInMinutes" : 20^
@REM   }^
@REM } > appsettings.json

@REM mkdir Dtos  
@REM mkdir Profile  
@REM cd Profile 
@REM echo using AutoMapper;^
@REM using Dominio.Entities;^
@REM using Api%file_name%.Dtos;^
@REM ^
@REM namespace Api%file_name%.Profiles;^
@REM     public class MappingProfiles : Profile{^
@REM ^
@REM         public MappingProfiles(){^
@REM             CreateMap<Alumno, AlumnoDto>()^
@REM                 .ReverseMap();^
@REM ^
@REM             /* .ForMember(p => p.Profesores) */^
@REM         }^
@REM     } > MappingProfiles.cs
@REM cd ..

@REM cd Properties
@REM echo {^
@REM   "$schema": "https://json.schemastore.org/launchsettings.json",^
@REM   "iisSettings": {^
@REM     "windowsAuthentication": false,^
@REM     "anonymousAuthentication": true,^
@REM     "iisExpress": {^
@REM       "applicationUrl": "http://localhost:56880",^
@REM       "sslPort": 44381^
@REM     }^
@REM   },^
@REM   "profiles": {^
@REM     "http": {^
@REM       "commandName": "Project",^
@REM       "dotnetRunMessages": true,^
@REM       "launchBrowser": true,^
@REM       "launchUrl": "swagger",^
@REM       "applicationUrl": "http://localhost:5000",^
@REM       "environmentVariables": {^
@REM         "ASPNETCORE_ENVIRONMENT": "Development"^
@REM       }^
@REM     },^
@REM     "https": {^
@REM       "commandName": "Project",^
@REM       "dotnetRunMessages": true,^
@REM       "launchBrowser": true,^
@REM       "launchUrl": "swagger",^
@REM       "applicationUrl": "https://localhost:5001;http://localhost:5000",^
@REM       "environmentVariables": {^
@REM         "ASPNETCORE_ENVIRONMENT": "Development"^
@REM       }^
@REM     },^
@REM     "IIS Express": {^
@REM       "commandName": "IISExpress",^
@REM       "launchBrowser": true,^
@REM       "launchUrl": "swagger",^
@REM       "environmentVariables": {^
@REM         "ASPNETCORE_ENVIRONMENT": "Development"^
@REM       }^
@REM     }^
@REM   }^
@REM } > launchSettings.json

@REM cd ..
@REM mkdir Helpers
@REM cd ..

@REM echo "Se ha creado toda la estructura base del proyecto"
