function Get-FolderContent {
    param (
        [string]$FolderPath,
        [string]$Prefix = "",
        [System.Windows.Forms.TreeView]$TreeView,
        [System.Windows.Forms.TreeNode]$ParentNode
    )
    
    $items = Get-ChildItem $FolderPath

    foreach ($item in $items) {
        $nodeName = $item.Name
        if ($item.PSIsContainer) {
            $nodeName = "📁 $nodeName"
        } else {
            $sizeInMB = [math]::Round(($item.Length / 1MB), 2)
            $nodeName = "📄 $nodeName ($sizeInMB MB)"
        }

        $newNode = New-Object System.Windows.Forms.TreeNode
        $newNode.Text = $nodeName
        $newNode.Tag = $item.FullName

        if ($ParentNode) {
            $ParentNode.Nodes.Add($newNode) | Out-Null
        } else {
            $TreeView.Nodes.Add($newNode) | Out-Null
        }

        if ($item.PSIsContainer) {
            Get-FolderContent -FolderPath $item.FullName -Prefix "$Prefix  " -TreeView $TreeView -ParentNode $newNode
        }
    }
}

function Show-FolderBrowser {
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowser.Description = "Seleccione la carpeta raíz"
    $folderBrowser.RootFolder = [System.Environment+SpecialFolder]::MyComputer

    if ($folderBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        return $folderBrowser.SelectedPath
    }
    return $null
}

function Show-FileDetails {
    param (
        [string]$FilePath
    )

    $item = Get-Item $FilePath
    $sizeInMB = [math]::Round(($item.Length / 1MB), 2)

    $details = @"
Nombre: $($item.Name)
Tamaño: $sizeInMB MB
Última modificación: $($item.LastWriteTime)
Ruta completa: $($item.FullName)
"@

    [System.Windows.Forms.MessageBox]::Show($details, "Detalles del archivo", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
}

# Cargar los ensamblados necesarios
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Crear el formulario principal
$form = New-Object System.Windows.Forms.Form
$form.Text = "Explorador de Carpetas"
$form.Size = New-Object System.Drawing.Size(800, 600)

# Crear el TreeView
$treeView = New-Object System.Windows.Forms.TreeView
$treeView.Dock = [System.Windows.Forms.DockStyle]::Fill
$treeView.Add_NodeMouseDoubleClick({
    $node = $_.Node
    if (Test-Path $node.Tag -PathType Leaf) {
        Show-FileDetails -FilePath $node.Tag
    }
})

# Crear el botón para seleccionar la carpeta
$btnSelectFolder = New-Object System.Windows.Forms.Button
$btnSelectFolder.Text = "Seleccionar Carpeta"
$btnSelectFolder.Dock = [System.Windows.Forms.DockStyle]::Top
$btnSelectFolder.Add_Click({
    $selectedPath = Show-FolderBrowser
    if ($selectedPath) {
        $treeView.Nodes.Clear()
        Get-FolderContent -FolderPath $selectedPath -TreeView $treeView
    }
})

# Agregar controles al formulario
$form.Controls.Add($treeView)
$form.Controls.Add($btnSelectFolder)

# Mostrar el formulario
$form.ShowDialog()