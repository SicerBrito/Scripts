import os
import subprocess

# Función para mostrar el menú y obtener el nombre del archivo
def get_file_name():
    file_name = input("Ingrese el nombre que va a tener archivo/carpeta: ")
    return file_name

# Función para crar la carpeta que va a contener todo el proyecto
def create_project_folder(folder_name):
    os.mkdir(folder_name)
    os.chdir(folder_name)

# Función para crear una nueva aplicación webapi con dotnet
def create_webapi(project_name):
    subprocess.run(["dotnet", "new", "webapi", "-o", f"Api{project_name}"])
    os.chdir(f"Api{project_name}")

    # Crear la estructura de carpetas y archivos
    subprocess.run(["dotnet", "new", "sln"])
    subprocess.run(["dotnet", "new", "classlib", "-o", "Dominio"])
    subprocess.run(["dotnet", "new", "classlib", "-o", "Persistencia"])
    subprocess.run(["dotnet", "new", "classlib", "-o", "Aplicacion"])
    subprocess.run(["dotnet", "new", "classlib", "-o", "Seguridad"])
    subprocess.run(["dotnet", "sln", "add", "Dominio"])
    subprocess.run(["dotnet", "sln", "add", "Aplicacion"])
    subprocess.run(["dotnet", "sln", "add", "Seguridad"])
    subprocess.run(["dotnet", "sln", "add", f"Api{project_name}"])

    # Crear las referencias
    os.chdir("Persistencia")
    subprocess.run(["dotnet", "add", "reference", "..\\Dominio\\"])
    os.chdir("..")

    os.chdir("Aplicacion")
    subprocess.run(["dotnet", "add", "reference", "..\\Dominio\\"])
    subprocess.run(["dotnet", "add", "reference", "..\\Persistencia\\"])
    os.chdir("..")

    os.chdir("Seguridad")
    subprocess.run(["dotnet", "add", "reference", "..\\Aplicacion\\"])
    os.chdir("..")

    os.chdir(f"Api{project_name}")
    subprocess.run(["dotnet", "add", "reference", "..\\Aplicacion\\"])
    subprocess.run(["dotnet", "add", "reference", "..\\Seguridad\\"])
    os.chdir("..")

    # Instalación de herramientas
    os.chdir("Dominio")
    subprocess.run(["dotnet", "add", "package", "Microsoft.EntityFrameworkCore", "--version", "7.0.10"])
    subprocess.run(["dotnet", "add", "package", "MediatR.Extensions.Microsoft.DependencyInjection", "--version", "11.1.0"])
    subprocess.run(["dotnet", "add", "package", "AutoMapper.Extensions.Microsoft.DependencyInjection", "--version", "12.0.1"])
    subprocess.run(["dotnet", "add", "package", "FluentValidation.AspNetCore", "--version", "11.3.0"])
    subprocess.run(["dotnet", "add", "package", "itext7.pdfhtml", "--version", "5.0.1"])
    os.chdir("..")

    os.chdir("Persistencia")
    subprocess.run(["dotnet", "add", "package", "Microsoft.EntityFrameworkCore", "--version", "7.0.10"])
    subprocess.run(["dotnet", "add", "package", "Pomelo.EntityFrameworkCore.MySql", "--version", "7.0.0"])
    subprocess.run(["dotnet", "add", "package", "Dapper", "--version", "2.0.151"])
    os.chdir("..")

    os.chdir("Seguridad")
    subprocess.run(["dotnet", "add", "package", "System.IdentityModel.Tokens.Jwt", "--version", "6.32.2"])
    os.chdir("..")

    os.chdir(f"Api{project_name}")
    subprocess.run(["dotnet", "add", "package", "Microsoft.EntityFrameworkCore.Design", "--version", "7.0.10"])
    subprocess.run(["dotnet", "add", "package", "Newtonsoft.Json", "--version", "13.0.3"])
    subprocess.run(["dotnet", "add", "package", "Microsoft.AspNetCore.Authentication.JwtBearer", "--version", "7.0.10"])
    subprocess.run(["dotnet", "add", "package", "Swashbuckle.AspNetCore", "--version", "6.5.0"])
    os.chdir("..")

    # Crear la estructura de los archivos dentro de Dominio
    os.chdir("Dominio")
    os.mkdir("Entities")
    os.chdir("Entities")

    with open("BaseEntity.cs", "w") as file:
        file.write('namespace Dominio.Entities;\n'
                   'public class BaseEntity{\n'
                   '\n'
                   '    public int Id { get; set; }\n'
                   '\n'
                   '}')
    
    with open("BaseEntityA.cs", "w") as file:
        file.write('namespace Dominio.Entities;\n'
                   'public class BaseEntityA{\n'
                   '\n'
                   '    public string ? Id { get; set; }\n'
                   '\n'
                   '}')

    os.chdir("..")

    os.mkdir("Interfaces")
    os.chdir("Interfaces")

    with open("IGenericRepository.cs", "w") as file:
        file.write('using System.Linq.Expressions;\n'
                   'using Dominio.Entities;\n'
                   '\n'
                   'namespace Dominio.Interfaces;\n'
                   '    public interface IGenericRepository<T> where T : BaseEntity{\n'
                   '\n'
                   '        Task<T> ? GetByIdAsync(string Id);\n'
                   '        Task<IEnumerable<T>> GetAllAsync();\n'
                   '        IEnumerable<T> Find(Expression<Func<T, bool>> expression);\n'
                   '        void Add(T entity);\n'
                   '        void AddRange(IEnumerable<T> entities);\n'
                   '        void Remove(T entity);\n'
                   '        void RemoveRange(IEnumerable<T> entities);\n'
                   '        void Update(T entity);\n'
                   '\n'
                   '    }')
    
    with open("IUnitOfWork.cs", "w") as file:
        file.write('namespace Dominio.Interfaces;\n'
                   '    public interface IUnitOfWork{\n'
                   '        INombreInterfas ? PluralInterfas { get; }\n'
                   '        Task<int> SaveAsync();\n'
                   '    }')

    os.chdir("..")
    os.chdir("..")

    print("Se ha creado la estructura base del proyecto")

# Función para crear una nueva entidad
def create_entity():
    file_name = get_file_name()

    os.chdir("Dominio")
    os.chdir("Entities")

    with open(f"{file_name}.cs", "w") as file:
        file.write(f'namespace Dominio.Entities;\n'
                   f'public class {file_name} : BaseEntity{{\n'
                   f'\n'
                   f'    public ICollection<Profesor> ? Profesores {{ get; set; }} = new HashSet<Profesor>();\n'
                   f'    public ICollection<Salon> ? Salones {{ get; set; }}\n'
                   f'}}')

    os.chdir("..")
    os.chdir("..")

    print(f"Se ha creado la entidad {file_name}")

# Función para crear un nuevo archivo context
def create_context():
    file_name = get_file_name()

    os.chdir("Persistencia")
    os.chdir("Data")

    with open(f"{file_name}Context.cs", "w") as file:
        file.write('using System.Reflection;\n'
                   'using Dominio.Entities;\n'
                   'using Microsoft.EntityFrameworkCore;\n'
                   '\n'
                   'namespace Persistencia.Data;\n'
                   f'public class {file_name}Context : DbContext{{\n'
                   f'    public {file_name}Context(DbContextOptions<{file_name}Context> options) : base(options){{\n'
                   f'\n'
                   f'    }}\n'
                   '\n'
                   f'    public DbSet<{file_name}> NombreEnPlural {{ get; set; }} = null!;\n'
                   '\n'
                   f'    protected override void OnModelCreating(ModelBuilder modelBuilder){{\n'
                   f'        base.OnModelCreating(modelBuilder);\n'
                   f'        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());\n'
                   f'    }}\n'
                   '}')
    
    os.mkdir("Configuration")
    os.chdir("Configuration")

    with open(f"{file_name}Configuration.cs", "w") as file:
        file.write('using Dominio.Entities;\n'
                   'using Microsoft.EntityFrameworkCore;\n'
                   'using Microsoft.EntityFrameworkCore.Metadata;\n'
                   'using Microsoft.EntityFrameworkCore.Metadata.Builders;\n'
                   '\n'
                   'namespace Persistencia.Data.Configuration;\n'
                   f'public class {file_name}Configuration : IEntityTypeConfiguration<{file_name}>\n'
                   '{\n'
                   f'    public void Configure(EntityTypeBuilder<{file_name}> builder)\n'
                   '    {\n'
                   f'        builder.ToTable("{file_name}");\n'
                   '\n'
                   f'        builder.Property(p => p.)\n'
                   '            .HasAnnotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn)\n'
                   '            .HasColumnName("")\n'
                   '            .HasColumnType("")\n'
                   '            .IsRequired();\n'
                   '\n'
                   f'        builder.Property(p => p.)\n'
                   '            .HasColumnName("")\n'
                   '            .HasColumnType("")\n'
                   '            .HasMaxLength()\n'
                   '            .IsRequired();\n'
                   '\n'
                   f'        builder.HasOne(p => p.)\n'
                   '            .WithMany(p => p.)\n'
                   '            .HasForeignKey(p => p.);\n'
                   '\n'
                   f'        builder.HasMany(p => p.)\n'
                   '            .WithMany(p => p.)\n'
                   '            .UsingEntity<>\n'
                   '            (\n'
                   f'                p => p\n'
                   '                    .HasOne(p => p.)\n'
                   '                    .WithMany(p => p.)\n'
                   '                    .HasForeignKey(p => p.),\n'
                   '                p => p\n'
                   '                    .HasOne(p => p.)\n'
                   '                    .WithMany(p => p.)\n'
                   '                    .HasForeignKey(p => p.),\n'
                   '                p => {\n'
                   f'                    p.HasKey(p=> new {{p.,p.}});\n'
                   '                }\n'
                   '            );\n'
                   '    }\n'
                   '}')
    
    os.chdir("..")
    os.chdir("..")
    os.chdir("..")

    print(f"Se ha creado el archivo {file_name}Context")
    
# Función para crear un nuevo archivo de configuración
def create_configuración():
    file_name = get_file_name()

    os.chdir("Persistencia")
    os.chdir("Data")
    os.chdir("Configuration")

    with open(f"{file_name}Configuration.cs", "w") as file:
        file.write('using Dominio.Entities;\n'
                   'using Microsoft.EntityFrameworkCore;\n'
                   'using Microsoft.EntityFrameworkCore.Metadata;\n'
                   'using Microsoft.EntityFrameworkCore.Metadata.Builders;\n'
                   '\n'
                   'namespace Persistencia.Data.Configuration;\n'
                   f'public class {file_name}Configuration : IEntityTypeConfiguration<{file_name}>\n'
                   '{\n'
                   f'    public void Configure(EntityTypeBuilder<{file_name}> builder)\n'
                   '    {\n'
                   f'        builder.ToTable("{file_name}");\n'
                   '\n'
                   f'        builder.Property(p => p.)\n'
                   '            .HasAnnotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn)\n'
                   '            .HasColumnName("")\n'
                   '            .HasColumnType("")\n'
                   '            .IsRequired();\n'
                   '\n'
                   f'        builder.Property(p => p.)\n'
                   '            .HasColumnName("")\n'
                   '            .HasColumnType("")\n'
                   '            .HasMaxLength()\n'
                   '            .IsRequired();\n'
                   '\n'
                   f'        builder.HasOne(p => p.)\n'
                   '            .WithMany(p => p.)\n'
                   '            .HasForeignKey(p => p.);\n'
                   '\n'
                   f'        builder.HasMany(p => p.)\n'
                   '            .WithMany(p => p.)\n'
                   '            .UsingEntity<>\n'
                   '            (\n'
                   f'                p => p\n'
                   '                    .HasOne(p => p.)\n'
                   '                    .WithMany(p => p.)\n'
                   '                    .HasForeignKey(p => p.),\n'
                   '                p => p\n'
                   '                    .HasOne(p => p.)\n'
                   '                    .WithMany(p => p.)\n'
                   '                    .HasForeignKey(p => p.),\n'
                   '                p => {\n'
                   f'                    p.HasKey(p=> new {{p.,p.}});\n'
                   '                }\n'
                   '            );\n'
                   '    }\n'
                   '}')
    
    os.chdir("..")
    os.chdir("..")
    os.chdir("..")

    print(f"Se ha creado el archivo {file_name}Configuration")

# Función para crear una nueva interfaz
def create_interface():
    file_name = get_file_name()

    os.chdir("Dominio")
    os.chdir("Interfaces")

    with open(f"I{file_name}Repository.cs", "w") as file:
        file.write('using Dominio.Entities;\n'
                   '\n'
                   f'namespace Dominio.Interfaces;\n'
                   f'    public interface I{file_name}Repository : IGenericRepository<{file_name}>{{\n'
                   f'    }}')

    os.chdir("..")
    os.chdir("..")

    print(f"Se ha creado la interfaz I{file_name}")

# Función para crear un nuevo repositorio
def create_repository():
    file_name = get_file_name()

    os.chdir("Aplicacion")
    os.chdir("Repository")

    with open(f"{file_name}Repository.cs", "w") as file:
        file.write('using Dominio.Entities;\n'
                   'using Dominio.Interfaces;\n'
                   'using Persistencia.Data;\n'
                   'using Microsoft.EntityFrameworkCore;\n'
                   '\n'
                   f'namespace Aplicacion.Repository;\n'
                   f'public class {file_name}Repository : GenericRepository<{file_name}>, I{file_name}Repository\n'
                   '{\n'
                   '    private readonly NameContext _Context;\n'
                   f'    public {file_name}Repository(NameContext context) : base(context)\n'
                   '    {\n'
                   '        _Context = context;\n'
                   '    }\n'
                   '\n'
                   '\n'
                   '    public override async Task<IEnumerable<{file_name}>> GetAllAsync()\n'
                   '    {\n'
                   f'        return await _Context.{file_name}s\n'
                   '            .Include(p => (p.Profesores as List<Profesor>).Select(i=>i.Nombre))\n'
                   '            .ToListAsync();\n'
                   '    }\n'
                   '\n'
                   '}')
    
    os.chdir("..")
    os.chdir("..")

    print(f"Se ha creado el repositorio {file_name}")

# Main
while True:
    os.system("clear")
    print("-------------------------------- Menu Proyecto --------------------------------")
    print("Recuerde comenzar el nombre de los archivos o carpetas con la primera letra en Mayúscula")
    print("1. Crear la carpeta del Proyecto")
    print("2. Crear la aplicación WebApi junto al resto de la estructura")
    print("3. Crear el archivo context dentro de la carpeta Data")
    print("4. Crear los archivos Entidades dentro de la carpeta Dominio")
    print("5. Crear los archivos Configuraciones dentro de la carpeta Persistencia/Data/Configurations")
    print("6. Crear los archivos Interfaces dentro de la carpeta Dominio/Interfaces")
    print("7. Crear los archivos Repositorios dentro de la carpeta Aplicacion/Repository")
    print("8. Crear los archivos Dtos dentro de la carpeta WebApi")
    print("9. Crear los archivos Controllers dentro de la carpeta WebApi")
    print("10. Salir")
    choice = input("Seleccione una opción: ")

    if choice == '1':
        # Carpeta del proyecto
        folder_name = get_file_name()
        create_project_folder(folder_name)
        print(f"Se ha creado la carpeta {folder_name}")
    elif choice == '2':
        # Estructura base y WebApi
        project_name = get_file_name()
        create_webapi(project_name)
    elif choice == '3':
        # Archivo context y las carpetas Data y Configuration
        create_context()
    elif choice == '4':
        # Crear Entidad dentro de Dominio/Entities
        create_entity()
    elif choice == '5':
        # Crear Canfiguracion dentro de Data/Configuration
        create_configuración()
    elif choice == '6':
        # Crear Interfas dentro de Dominio/Interfaces
        create_interface()
    elif choice == '7':
        # Crear Repositorio dentro de la carpeta Aplicacion/Repository
        create_repository()
    elif choice == '8':
        # Crear Dto dentro de la carpeta WebApi/Dtos
        pass
    elif choice == '9':
        # Crear Controller dentro de la carpeta WebApi/Controllers
        pass
    elif choice == '10':
        # Salir del Menu
        print("Saliendo...")
        break
    else:
        print("Opción no válida")
    
    input("Presione Enter para continuar...")
