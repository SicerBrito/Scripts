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

echo "## Ignore Visual Studio temporary files, build results, and
## files generated by popular Visual Studio add-ons.
##
## Get latest from https://github.com/github/gitignore/blob/main/VisualStudio.gitignore

# User-specific files
*.rsuser
*.suo
*.user
*.userosscache
*.sln.docstates

# User-specific files (MonoDevelop/Xamarin Studio)
*.userprefs

# Mono auto generated files
mono_crash.*

# Build results
[Dd]ebug/
[Dd]ebugPublic/
[Rr]elease/
[Rr]eleases/
x64/
x86/
[Ww][Ii][Nn]32/
[Aa][Rr][Mm]/
[Aa][Rr][Mm]64/
bld/
[Bb]in/
[Oo]bj/
[Ll]og/
[Ll]ogs/

# Visual Studio 2015/2017 cache/options directory
.vs/
# Uncomment if you have tasks that create the project's static files in wwwroot
#wwwroot/

# Visual Studio 2017 auto generated files
Generated\ Files/

# MSTest test Results
[Tt]est[Rr]esult*/
[Bb]uild[Ll]og.*

# NUnit
*.VisualState.xml
TestResult.xml
nunit-*.xml

# Build Results of an ATL Project
[Dd]ebugPS/
[Rr]eleasePS/
dlldata.c

# Benchmark Results
BenchmarkDotNet.Artifacts/

# .NET Core
project.lock.json
project.fragment.lock.json
artifacts/

# ASP.NET Scaffolding
ScaffoldingReadMe.txt

# StyleCop
StyleCopReport.xml

# Files built by Visual Studio
*_i.c
*_p.c
*_h.h
*.ilk
*.meta
*.obj
*.iobj
*.pch
*.pdb
*.ipdb
*.pgc
*.pgd
*.rsp
*.sbr
*.tlb
*.tli
*.tlh
*.tmp
*.tmp_proj
*_wpftmp.csproj
*.log
*.tlog
*.vspscc
*.vssscc
.builds
*.pidb
*.svclog
*.scc

# Chutzpah Test files
_Chutzpah*

# Visual C++ cache files
ipch/
*.aps
*.ncb
*.opendb
*.opensdf
*.sdf
*.cachefile
*.VC.db
*.VC.VC.opendb

# Visual Studio profiler
*.psess
*.vsp
*.vspx
*.sap

# Visual Studio Trace Files
*.e2e

# TFS 2012 Local Workspace
$tf/

# Guidance Automation Toolkit
*.gpState

# ReSharper is a .NET coding add-in
_ReSharper*/
*.[Rr]e[Ss]harper
*.DotSettings.user

# TeamCity is a build add-in
_TeamCity*

# DotCover is a Code Coverage Tool
*.dotCover

# AxoCover is a Code Coverage Tool
.axoCover/*
!.axoCover/settings.json

# Coverlet is a free, cross platform Code Coverage Tool
coverage*.json
coverage*.xml
coverage*.info

# Visual Studio code coverage results
*.coverage
*.coveragexml

# NCrunch
_NCrunch_*
.*crunch*.local.xml
nCrunchTemp_*

# MightyMoose
*.mm.*
AutoTest.Net/

# Web workbench (sass)
.sass-cache/

# Installshield output folder
[Ee]xpress/

# DocProject is a documentation generator add-in
DocProject/buildhelp/
DocProject/Help/*.HxT
DocProject/Help/*.HxC
DocProject/Help/*.hhc
DocProject/Help/*.hhk
DocProject/Help/*.hhp
DocProject/Help/Html2
DocProject/Help/html

# Click-Once directory
publish/

# Publish Web Output
*.[Pp]ublish.xml
*.azurePubxml
# Note: Comment the next line if you want to checkin your web deploy settings,
# but database connection strings (with potential passwords) will be unencrypted
*.pubxml
*.publishproj

# Microsoft Azure Web App publish settings. Comment the next line if you want to
# checkin your Azure Web App publish settings, but sensitive information contained
# in these scripts will be unencrypted
PublishScripts/

# NuGet Packages
*.nupkg
# NuGet Symbol Packages
*.snupkg
# The packages folder can be ignored because of Package Restore
**/[Pp]ackages/*
# except build/, which is used as an MSBuild target.
!**/[Pp]ackages/build/
# Uncomment if necessary however generally it will be regenerated when needed
#!**/[Pp]ackages/repositories.config
# NuGet v3's project.json files produces more ignorable files
*.nuget.props
*.nuget.targets

# Microsoft Azure Build Output
csx/
*.build.csdef

# Microsoft Azure Emulator
ecf/
rcf/

# Windows Store app package directories and files
AppPackages/
BundleArtifacts/
Package.StoreAssociation.xml
_pkginfo.txt
*.appx
*.appxbundle
*.appxupload

# Visual Studio cache files
# files ending in .cache can be ignored
*.[Cc]ache
# but keep track of directories ending in .cache
!?*.[Cc]ache/

# Others
ClientBin/
~$*
*~
*.dbmdl
*.dbproj.schemaview
*.jfm
*.pfx
*.publishsettings
orleans.codegen.cs

# Including strong name files can present a security risk
# (https://github.com/github/gitignore/pull/2483#issue-259490424)
#*.snk

# Since there are multiple workflows, uncomment next line to ignore bower_components
# (https://github.com/github/gitignore/pull/1529#issuecomment-104372622)
#bower_components/

# RIA/Silverlight projects
Generated_Code/

# Backup & report files from converting an old project file
# to a newer Visual Studio version. Backup files are not needed,
# because we have git ;-)
_UpgradeReport_Files/
Backup*/
UpgradeLog*.XML
UpgradeLog*.htm
ServiceFabricBackup/
*.rptproj.bak

# SQL Server files
*.mdf
*.ldf
*.ndf

# Business Intelligence projects
*.rdl.data
*.bim.layout
*.bim_*.settings
*.rptproj.rsuser
*- [Bb]ackup.rdl
*- [Bb]ackup ([0-9]).rdl
*- [Bb]ackup ([0-9][0-9]).rdl

# Microsoft Fakes
FakesAssemblies/

# GhostDoc plugin setting file
*.GhostDoc.xml

# Node.js Tools for Visual Studio
.ntvs_analysis.dat
node_modules/

# Visual Studio 6 build log
*.plg

# Visual Studio 6 workspace options file
*.opt

# Visual Studio 6 auto-generated workspace file (contains which files were open etc.)
*.vbw

# Visual Studio 6 auto-generated project file (contains which files were open etc.)
*.vbp

# Visual Studio 6 workspace and project file (working project files containing files to include in project)
*.dsw
*.dsp

# Visual Studio 6 technical files
*.ncb
*.aps

# Visual Studio LightSwitch build output
**/*.HTMLClient/GeneratedArtifacts
**/*.DesktopClient/GeneratedArtifacts
**/*.DesktopClient/ModelManifest.xml
**/*.Server/GeneratedArtifacts
**/*.Server/ModelManifest.xml
_Pvt_Extensions

# Paket dependency manager
.paket/paket.exe
paket-files/

# FAKE - F# Make
.fake/

# CodeRush personal settings
.cr/personal

# Python Tools for Visual Studio (PTVS)
__pycache__/
*.pyc

# Cake - Uncomment if you are using it
# tools/**
# !tools/packages.config

# Tabs Studio
*.tss

# Telerik's JustMock configuration file
*.jmconfig

# BizTalk build output
*.btp.cs
*.btm.cs
*.odx.cs
*.xsd.cs

# OpenCover UI analysis results
OpenCover/

# Azure Stream Analytics local run output
ASALocalRun/

# MSBuild Binary and Structured Log
*.binlog

# NVidia Nsight GPU debugger configuration file
*.nvuser

# MFractors (Xamarin productivity tool) working folder
.mfractor/

# Local History for Visual Studio
.localhistory/

# Visual Studio History (VSHistory) files
.vshistory/

# BeatPulse healthcheck temp database
healthchecksdb

# Backup folder for Package Reference Convert tool in Visual Studio 2017
MigrationBackup/

# Ionide (cross platform F# VS Code tools) working folder
.ionide/

# Fody - auto-generated XML schema
FodyWeavers.xsd

# VS Code files for those working on multiple tools
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
*.code-workspace

# Local History for Visual Studio Code
.history/

# Windows Installer files from build outputs
*.cab
*.msi
*.msix
*.msm
*.msp

# JetBrains Rider
*.sln.iml
" > .gitignore

echo "Se ha creado toda la estructura base del proyecto"

}

# Función para crear una nueva entidad
create_entity() {
    
cd Dominio 
cd Entities  

echo "namespace Dominio.Entities;
public class "$file_name" : BaseEntity{

    public ICollection<Profesor> ? Profesores { get; set; } = new HashSet<Profesor>();
    public ICollection<Salon> ? Salones { get; set;}
}" > "$file_name".cs

cd ..
cd ..
}

# Función para crear un nuevo archivo context
create_context() {
cd Persistencia  
mkdir Data 
cd Data

echo "using System.Reflection;
using Dominio.Entities;
using Microsoft.EntityFrameworkCore;

namespace Persistencia.Data;
public class "$file_name"Context : DbContext{
    public "$file_name"Context(DbContextOptions<"$file_name"Context> options) : base(options){

    }

    public DbSet<NombreEntidad> NombreEnPlural { get; set; } = null!;

    protected override void OnModelCreating(ModelBuilder modelBuilder){
        base.OnModelCreating(modelBuilder);
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }
}" > "$file_name"Context.cs

mkdir Configuration 
cd ..
cd ..
}

# Función para crear un nuevo archivo de configuración
create_configuración() {

cd Persistencia
cd Data
cd Configuration

echo "using Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Persistencia.Data.Configuration;
public class "$file_name"Configuration : IEntityTypeConfiguration<{"$file_name"}>
{
    public void Configure(EntityTypeBuilder<{"$file_name"}> builder)
    {
        builder.ToTable(""$file_name"");

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
}" > "$file_name"Configuration.cs

cd ..
cd ..
cd ..

}

create_interface() {
cd Dominio
cd Interfaces

echo "using Dominio.Entities;

namespace Dominio.Interfaces;
    public interface I"$file_name"Repository : IGenericRepository<"$file_name">{
        
    }" > I"$file_name"Repository.cs

cd ..
cd ..
}

create_repository() {
cd Aplicacion
cd Repository

echo "using Dominio.Entities;
using Dominio.Interfaces;
using Persistencia.Data;
using Microsoft.EntityFrameworkCore;
namespace Aplicacion.Repository;
public class "$file_name"Repository : GenericRepository<"$file_name">, I"$file_name"Repository
{
    private readonly NameContext _Context;
    public "$file_name"Repository(NameContext context) : base(context)
    {
        _Context = context;
    }


    public override async Task<IEnumerable<"$file_name">> GetAllAsync()
    {
        return await _Context."$file_name"s
            .Include(p => (p.Profesores as List<Profesor>).Select(i=>i.Nombre)) //Si no se coloca en la parte del json apareceria como null            
            .ToListAsync();
    }

}" > "$file_name"Repository.cs

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