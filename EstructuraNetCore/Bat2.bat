@echo off
:menu
cls
echo -------------------------------- Menu Proyecto --------------------------------
echo Recuerde comenzar el nombre de los archivos o carpetas con la primera letra en Mayúscula
echo 1. Crear la carpeta del Proyecto
echo 2. Crear la aplicación WebApi junto al resto de la estructura
echo 3. Crear el archivo context dentro de la carpeta Data
echo 4. Crear los archivos Entidades dentro de la carpeta Dominio
echo 5. Crear los archivos Configuraciones dentro de la carpeta Persistencia/Data/Configurations
echo 6. Crear los archivos Interfaces dentro de la carpeta Dominio/Interfaces
echo 7. Crear los archivos Repositorios dentro de la carpeta Aplicacion/Repository
echo 8. Crear los archivos Dtos dentro de la carpeta WebApi
echo 9. Crear los archivos Controllers dentro de la carpeta WebApi
echo 10. Salir

set /p choice=Seleccione una opción: 

if "%choice%"=="1" (
    rem Carpeta del proyecto
    set /p "folder_name=Ingrese el nombre que va a tener archivo/carpeta: "
    mkdir "%folder_name%"
    cd "%folder_name%"
    echo Se ha creado la carpeta %folder_name%
    pause
    goto menu
) elseif "%choice%"=="2" (
    rem Estructura base y WebApi
    set /p "project_name=Ingrese el nombre que va a tener el proyecto WebApi: "
    dotnet new webapi -o "Api%project_name%"
    cd "Api%project_name%"

    rem Crear la estructura de carpetas y archivos
    dotnet new sln
    dotnet new classlib -o "Dominio"
    dotnet new classlib -o "Persistencia"
    dotnet new classlib -o "Aplicacion"
    dotnet new classlib -o "Seguridad"
    dotnet sln add "Dominio"
    dotnet sln add "Aplicacion"
    dotnet sln add "Seguridad"
    dotnet sln add "Api%project_name%"

    rem Crear las referencias
    cd "Persistencia"
    dotnet add reference "..\Dominio\"
    cd ..

    cd "Aplicacion"
    dotnet add reference "..\Dominio\"
    dotnet add reference "..\Persistencia\"
    cd ..

    cd "Seguridad"
    dotnet add reference "..\Aplicacion\"
    cd ..

    cd "Api%project_name%"
    dotnet add reference "..\Aplicacion\"
    dotnet add reference "..\Seguridad\"
    cd ..

    rem Instalación de herramientas
    cd "Dominio"
    dotnet add package Microsoft.EntityFrameworkCore --version 7.0.10
    dotnet add package MediatR.Extensions.Microsoft.DependencyInjection --version 11.1.0
    dotnet add package AutoMapper.Extensions.Microsoft.DependencyInjection --version 12.0.1
    dotnet add package FluentValidation.AspNetCore --version 11.3.0
    dotnet add package itext7.pdfhtml --version 5.0.1
    cd ..

    cd "Persistencia"
    dotnet add package Microsoft.EntityFrameworkCore --version 7.0.10
    dotnet add package Pomelo.EntityFrameworkCore.MySql --version 7.0.0
    dotnet add package Dapper --version 2.0.151
    cd ..

    cd "Seguridad"
    dotnet add package System.IdentityModel.Tokens.Jwt --version 6.32.2
    cd ..

    cd "Api%project_name%"
    dotnet add package Microsoft.EntityFrameworkCore.Design --version 7.0.10
    dotnet add package Newtonsoft.Json --version 13.0.3
    dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer --version 7.0.10
    dotnet add package Swashbuckle.AspNetCore --version 6.5.0
    cd ..

    rem Crear la estructura de los archivos dentro de Dominio
    cd "Dominio"
    mkdir "Entities"
    cd "Entities"

    echo namespace Dominio.Entities;> BaseEntity.cs
    echo public class BaseEntity{>> BaseEntity.cs
    echo.>> BaseEntity.cs
    echo     public int Id { get; set; }>> BaseEntity.cs
    echo.>> BaseEntity.cs
    echo }>> BaseEntity.cs

    echo namespace Dominio.Entities;> BaseEntityA.cs
    echo public class BaseEntityA{>> BaseEntityA.cs
    echo.>> BaseEntityA.cs
    echo     public string ? Id { get; set; }>> BaseEntityA.cs
    echo.>> BaseEntityA.cs
    echo }>> BaseEntityA.cs

    cd ..

    mkdir "Interfaces"
    cd "Interfaces"

    echo using System.Linq.Expressions;> IGenericRepository.cs
    echo using Dominio.Entities;>> IGenericRepository.cs
    echo.>> IGenericRepository.cs
    echo namespace Dominio.Interfaces;>> IGenericRepository.cs
    echo     public interface IGenericRepository<T> where T : BaseEntity{>> IGenericRepository.cs
    echo.>> IGenericRepository.cs
    echo         Task<T> ? GetByIdAsync(string Id);>> IGenericRepository.cs
    echo         Task<IEnumerable<T>> GetAllAsync();>> IGenericRepository.cs
    echo         IEnumerable<T> Find(Expression<Func<T, bool>> expression);>> IGenericRepository.cs
    echo         void Add(T entity);>> IGenericRepository.cs
    echo         void AddRange(IEnumerable<T> entities);>> IGenericRepository.cs
    echo         void Remove(T entity);>> IGenericRepository.cs
    echo         void RemoveRange(IEnumerable<T> entities);>> IGenericRepository.cs
    echo         void Update(T entity);>> IGenericRepository.cs
    echo.>> IGenericRepository.cs
    echo     }>> IGenericRepository.cs

    echo namespace Dominio.Interfaces;> IUnitOfWork.cs
    echo     public interface IUnitOfWork{>> IUnitOfWork.cs
    echo         INombreInterfas ? PluralInterfas { get; }>> IUnitOfWork.cs
    echo         Task<int> SaveAsync();>> IUnitOfWork.cs
    echo     }>> IUnitOfWork.cs

    cd ..
    cd ..

    echo Se ha creado la estructura base del proyecto
    pause
    goto menu
) elseif "%choice%"=="3" (
    rem Archivo context y las carpetas Data y Configuration
    set /p "file_name=Ingrese el nombre que va a tener el archivo context: "
    cd "Persistencia"
    cd "Data"

    echo using System.Reflection;> %file_name%Context.cs
    echo using Dominio.Entities;>> %file_name%Context.cs
    echo using Microsoft.EntityFrameworkCore;>> %file_name%Context.cs
    echo.>> %file_name%Context.cs
    echo namespace Persistencia.Data;>> %file_name%Context.cs
    echo public class %file_name%Context : DbContext{>> %file_name%Context.cs
    echo     public %file_name%Context(DbContextOptions<%file_name%Context> options) : base(options){>> %file_name%Context.cs
    echo     }>> %file_name%Context.cs
    echo.>> %file_name%Context.cs
    echo     public DbSet<%file_name%> NombreEnPlural { get; set; } = null!;>> %file_name%Context.cs
    echo.>> %file_name%Context.cs
    echo     protected override void OnModelCreating(ModelBuilder modelBuilder){>> %file_name%Context.cs
    echo         base.OnModelCreating(modelBuilder);>> %file_name%Context.cs
    echo         modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());>> %file_name%Context.cs
    echo     }>> %file_name%Context.cs
    echo }>> %file_name%Context.cs

    mkdir "Configuration"
    cd "Configuration"

    echo using Dominio.Entities;> %file_name%Configuration.cs
    echo using Microsoft.EntityFrameworkCore;>> %file_name%Configuration.cs
    echo using Microsoft.EntityFrameworkCore.Metadata;>> %file_name%Configuration.cs
    echo using Microsoft.EntityFrameworkCore.Metadata.Builders;>> %file_name%Configuration.cs
    echo.>> %file_name%Configuration.cs
    echo namespace Persistencia.Data.Configuration;>> %file_name%Configuration.cs
    echo public class %file_name%Configuration : IEntityTypeConfiguration<%file_name%>>{>> %file_name%Configuration.cs
    echo     public void Configure(EntityTypeBuilder<%file_name%> builder){>> %file_name%Configuration.cs
    echo         builder.ToTable("%file_name%");>> %file_name%Configuration.cs
    echo.>> %file_name%Configuration.cs
    echo         builder.Property(p => p.)>> %file_name%Configuration.cs
    echo             .HasAnnotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn)>> %file_name%Configuration.cs
    echo             .HasColumnName("")>> %file_name%Configuration.cs
    echo             .HasColumnType("")>> %file_name%Configuration.cs
    echo             .IsRequired();>> %file_name%Configuration.cs
    echo.>> %file_name%Configuration.cs
    echo         builder.Property(p => p.)>> %file_name%Configuration.cs
    echo             .HasColumnName("")>> %file_name%Configuration.cs
    echo             .HasColumnType("")>> %file_name%Configuration.cs
    echo             .HasMaxLength()>> %file_name%Configuration.cs
    echo             .IsRequired();>> %file_name%Configuration.cs
    echo.>> %file_name%Configuration.cs
    echo         builder.HasOne(p => p.)>> %file_name%Configuration.cs
    echo             .WithMany(p => p.)>> %file_name%Configuration.cs
    echo             .HasForeignKey(p => p.);>> %file_name%Configuration.cs
    echo.>> %file_name%Configuration.cs
    echo         builder.HasMany(p => p.)>> %file_name%Configuration.cs
    echo             .WithMany(p => p.)>> %file_name%Configuration.cs
    echo             .UsingEntity<>> %file_name%Configuration.cs
    echo             (>> %file_name%Configuration.cs
    echo                 p => p>> %file_name%Configuration.cs
    echo                     .HasOne(p => p.)>> %file_name%Configuration.cs
    echo                     .WithMany(p => p.)>> %file_name%Configuration.cs
    echo                     .HasForeignKey(p => p.),>> %file_name%Configuration.cs
    echo                 p => p>> %file_name%Configuration.cs
    echo                     .HasOne(p => p.)>> %file_name%Configuration.cs
    echo                     .WithMany(p => p.)>> %file_name%Configuration.cs
    echo                     .HasForeignKey(p => p.),>> %file_name%Configuration.cs
    echo                 p => {>> %file_name%Configuration.cs
    echo                     p.HasKey(p=> new {p.,p.});>> %file_name%Configuration.cs
    echo                 }>> %file_name%Configuration.cs
    echo             );>> %file_name%Configuration.cs
    echo     }>> %file_name%Configuration.cs
    echo }>> %file_name%Configuration.cs

    cd ..
    cd ..
    cd ..

    echo Se ha creado el archivo %file_name%Context
    pause
    goto menu
) elseif "%choice%"=="4" (
    rem Crear Entidad dentro de Dominio/Entities
    set /p "file_name=Ingrese el nombre de la entidad: "
    cd "Dominio"
    cd "Entities"

    echo namespace Dominio.Entities;> %file_name%.cs
    echo public class %file_name% : BaseEntity{>> %file_name%.cs
    echo.>> %file_name%.cs
    echo     public ICollection<Profesor> ? Profesores { get; set; } = new HashSet<Profesor>();>> %file_name%.cs
    echo     public ICollection<Salon> ? Salones { get; set; }>> %file_name%.cs
    echo }>> %file_name%.cs

    cd ..
    cd ..

    echo Se ha creado la entidad %file_name%
    pause
    goto menu
) elseif "%choice%"=="5" (
    rem Crear Configuracion dentro de Data/Configuration
    set /p "file_name=Ingrese el nombre de la configuración: "
    cd "Persistencia"
    cd "Data"
    cd "Configuration"

    echo using Dominio.Entities;> %file_name%Configuration.cs
    echo using Microsoft.EntityFrameworkCore;>> %file_name%Configuration.cs
    echo using Microsoft.EntityFrameworkCore.Metadata;>> %file_name%Configuration.cs
    echo using Microsoft.EntityFrameworkCore.Metadata.Builders;>> %file_name%Configuration.cs
    echo.>> %file_name%Configuration.cs
    echo namespace Persistencia.Data.Configuration;>> %file_name%Configuration.cs
    echo public class %file_name%Configuration : IEntityTypeConfiguration<%file_name%>>{>> %file_name%Configuration.cs
    echo     public void Configure(EntityTypeBuilder<%file_name%> builder){>> %file_name%Configuration.cs
    echo         builder.ToTable("%file_name%");>> %file_name%Configuration.cs
    echo.>> %file_name%Configuration.cs
    echo         builder.Property(p => p.)>> %file_name%Configuration.cs
    echo             .HasAnnotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn)>> %file_name%Configuration.cs
    echo             .HasColumnName("")>> %file_name%Configuration.cs
    echo             .HasColumnType("")>> %file_name%Configuration.cs
    echo             .IsRequired();>> %file_name%Configuration.cs
    echo.>> %file_name%Configuration.cs
    echo         builder.Property(p => p.)>> %file_name%Configuration.cs
    echo             .HasColumnName("")>> %file_name%Configuration.cs
    echo             .HasColumnType("")>> %file_name%Configuration.cs
    echo             .HasMaxLength()>> %file_name%Configuration.cs
    echo             .IsRequired();>> %file_name%Configuration.cs
    echo.>> %file_name%Configuration.cs
    echo         builder.HasOne(p => p.)>> %file_name%Configuration.cs
    echo             .WithMany(p => p.)>> %file_name%Configuration.cs
    echo             .HasForeignKey(p => p.);>> %file_name%Configuration.cs
    echo.>> %file_name%Configuration.cs
    echo         builder.HasMany(p => p.)>> %file_name%Configuration.cs
    echo             .WithMany(p => p.)>> %file_name%Configuration.cs
    echo             .UsingEntity<>> %file_name%Configuration.cs
    echo             (>> %file_name%Configuration.cs
    echo                 p => p>> %file_name%Configuration.cs
    echo                     .HasOne(p => p.)>> %file_name%Configuration.cs
    echo                     .WithMany(p => p.)>> %file_name%Configuration.cs
    echo                     .HasForeignKey(p => p.),>> %file_name%Configuration.cs
    echo                 p => p>> %file_name%Configuration.cs
    echo                     .HasOne(p => p.)>> %file_name%Configuration.cs
    echo                     .WithMany(p => p.)>> %file_name%Configuration.cs
    echo                     .HasForeignKey(p => p.),>> %file_name%Configuration.cs
    echo                 p => {>> %file_name%Configuration.cs
    echo                     p.HasKey(p=> new {p.,p.});>> %file_name%Configuration.cs
    echo                 }>> %file_name%Configuration.cs
    echo             );>> %file_name%Configuration.cs
    echo     }>> %file_name%Configuration.cs
    echo }>> %file_name%Configuration.cs

    cd ..
    cd ..
    cd ..
    cd ..

    echo Se ha creado el archivo %file_name%Configuration
    pause
    goto menu
) elseif "%choice%"=="6" (
    rem Crear Interfas dentro de Dominio/Interfaces
    set /p "file_name=Ingrese el nombre de la interfaz: "
    cd "Dominio"
    cd "Interfaces"

    echo using Dominio.Entities;> I%file_name%Repository.cs
    echo.>> I%file_name%Repository.cs
    echo namespace Dominio.Interfaces;>> I%file_name%Repository.cs
    echo     public interface I%file_name%Repository : IGenericRepository<%file_name%>>{>> I%file_name%Repository.cs
    echo     }>> I%file_name%Repository.cs

    cd ..
    cd ..

    echo Se ha creado la interfaz I%file_name%
    pause
    goto menu
) elseif "%choice%"=="7" (
    rem Crear Repositorio dentro de la carpeta Aplicacion/Repository
    set /p "file_name=Ingrese el nombre del repositorio: "
    cd "Aplicacion"
    cd "Repository"

    echo using Dominio.Entities;> %file_name%Repository.cs
    echo using Dominio.Interfaces;>> %file_name%Repository.cs
    echo using Persistencia.Data;>> %file_name%Repository.cs
    echo using Microsoft.EntityFrameworkCore;>> %file_name%Repository.cs
    echo.>> %file_name%Repository.cs
    echo namespace Aplicacion.Repository;>> %file_name%Repository.cs
    echo public class %file_name%Repository : GenericRepository<%file_name%>, I%file_name%Repository{>> %file_name%Repository.cs
    echo     private readonly NameContext _Context;>> %file_name%Repository.cs
    echo     public %file_name%Repository(NameContext context) : base(context){>> %file_name%Repository.cs
    echo         _Context = context;>> %file_name%Repository.cs
    echo     }>> %file_name%Repository.cs
    echo.>> %file_name%Repository.cs
    echo     public override async Task<IEnumerable<%file_name%>> GetAllAsync(){>> %file_name%Repository.cs
    echo         return await _Context.%file_name%>> %file_name%Repository.cs
    echo             .Include(p => (p.Profesores as List<Profesor>).Select(i=>i.Nombre))>> %file_name%Repository.cs
    echo             .ToListAsync();>> %file_name%Repository.cs
    echo     }>> %file_name%Repository.cs
    echo }>> %file_name%Repository.cs

    cd ..
    cd ..

    echo Se ha creado el repositorio %file_name%
    pause
    goto menu
) elseif "%choice%"=="8" (
    rem Crear Dto dentro de la carpeta WebApi/Dtos
    rem Agrega aquí el código para crear Dto
) elseif "%choice%"=="9" (
    rem Crear Controller dentro de la carpeta WebApi/Controllers
    rem Agrega aquí el código para crear Controller
) elseif "%choice%"=="10" (
    rem Salir del Menú
    echo Saliendo...
    exit /b 0
) else (
    echo Opción no válida
    pause
    goto menu
)
