Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function Get-FolderContent {
    param (
        [string]$FolderPath,
        [System.Windows.Forms.TreeView]$TreeView,
        [System.Windows.Forms.TreeNode]$ParentNode
    )
    
    $items = Get-ChildItem $FolderPath -ErrorAction SilentlyContinue

    foreach ($item in $items) {
        $nodeName = $item.Name
        $icon = if ($item.PSIsContainer) { "folder" } else { "file" }
        $sizeInMB = if (!$item.PSIsContainer) { [math]::Round(($item.Length / 1MB), 2) } else { $null }

        $newNode = New-Object System.Windows.Forms.TreeNode
        $newNode.Text = "$nodeName $(if ($sizeInMB) { "($sizeInMB MB)" })"
        $newNode.Tag = @{
            FullPath = $item.FullName
            IsDirectory = $item.PSIsContainer
            Size = $sizeInMB
            LastModified = $item.LastWriteTime
        }
        $newNode.ImageKey = $icon
        $newNode.SelectedImageKey = $icon

        if ($ParentNode) {
            $ParentNode.Nodes.Add($newNode) | Out-Null
        } else {
            $TreeView.Nodes.Add($newNode) | Out-Null
        }

        if ($item.PSIsContainer) {
            $newNode.Nodes.Add((New-Object System.Windows.Forms.TreeNode))  # Placeholder
        }
    }
}

function Search-TreeView {
    param (
        [System.Windows.Forms.TreeView]$TreeView,
        [string]$SearchTerm
    )

    $foundNodes = New-Object System.Collections.ArrayList

    $searchNodes = {
        param($nodes)
        foreach ($node in $nodes) {
            if ($node.Text -like "*$SearchTerm*") {
                $foundNodes.Add($node) | Out-Null
            }
            if ($node.Nodes.Count -gt 0) {
                & $searchNodes $node.Nodes
            }
        }
    }

    & $searchNodes $TreeView.Nodes

    return $foundNodes
}

# Crear el formulario principal
$form = New-Object System.Windows.Forms.Form
$form.Text = "Explorador de Carpetas con Búsqueda Mejorada"
$form.Size = New-Object System.Drawing.Size(800, 600)

# Crear el panel de búsqueda
$searchPanel = New-Object System.Windows.Forms.Panel
$searchPanel.Dock = [System.Windows.Forms.DockStyle]::Top
$searchPanel.Height = 30

$searchBox = New-Object System.Windows.Forms.TextBox
$searchBox.Location = New-Object System.Drawing.Point(5, 5)
$searchBox.Size = New-Object System.Drawing.Size(680, 20)
$searchPanel.Controls.Add($searchBox)

$searchButton = New-Object System.Windows.Forms.Button
$searchButton.Location = New-Object System.Drawing.Point(690, 5)
$searchButton.Size = New-Object System.Drawing.Size(75, 20)
$searchButton.Text = "Buscar"
$searchPanel.Controls.Add($searchButton)

# Crear el TreeView
$treeView = New-Object System.Windows.Forms.TreeView
$treeView.Dock = [System.Windows.Forms.DockStyle]::Fill
$treeView.ImageList = New-Object System.Windows.Forms.ImageList
$treeView.ImageList.Images.Add("folder", [System.Drawing.SystemIcons]::Folder)
$treeView.ImageList.Images.Add("file", [System.Drawing.SystemIcons]::WinLogo)

$treeView.Add_BeforeExpand({
    $node = $_.Node
    if ($node.Nodes.Count -eq 1 -and $node.Nodes[0].Text -eq "") {
        $node.Nodes.Clear()
        Get-FolderContent -FolderPath $node.Tag.FullPath -TreeView $treeView -ParentNode $node
    }
})

# Crear el panel de detalles
$detailsPanel = New-Object System.Windows.Forms.Panel
$detailsPanel.Dock = [System.Windows.Forms.DockStyle]::Bottom
$detailsPanel.Height = 100

$detailsTextBox = New-Object System.Windows.Forms.TextBox
$detailsTextBox.Multiline = $true
$detailsTextBox.ReadOnly = $true
$detailsTextBox.Dock = [System.Windows.Forms.DockStyle]::Fill
$detailsPanel.Controls.Add($detailsTextBox)

# Función para mostrar detalles del nodo seleccionado
$treeView.Add_AfterSelect({
    $selectedNode = $treeView.SelectedNode
    if ($selectedNode) {
        $details = "Ruta: $($selectedNode.Tag.FullPath)`r`n"
        $details += "Tipo: $(if ($selectedNode.Tag.IsDirectory) { 'Carpeta' } else { 'Archivo' })`r`n"
        if ($selectedNode.Tag.Size) {
            $details += "Tamaño: $($selectedNode.Tag.Size) MB`r`n"
        }
        $details += "Última modificación: $($selectedNode.Tag.LastModified)"
        $detailsTextBox.Text = $details
    }
})

# Función de búsqueda
$performSearch = {
    $searchTerm = $searchBox.Text
    if ($searchTerm) {
        $foundNodes = Search-TreeView -TreeView $treeView -SearchTerm $searchTerm
        if ($foundNodes.Count -gt 0) {
            $treeView.SelectedNode = $foundNodes[0]
            $treeView.SelectedNode.EnsureVisible()
            $statusLabel.Text = "Se encontraron $($foundNodes.Count) resultados."
        } else {
            $statusLabel.Text = "No se encontraron resultados."
        }
    }
}

$searchButton.Add_Click($performSearch)
$searchBox.Add_KeyPress({
    if ($_.KeyChar -eq [char]13) {
        $performSearch.Invoke()
    }
})

# Crear el botón para seleccionar la carpeta
$btnSelectFolder = New-Object System.Windows.Forms.Button
$btnSelectFolder.Text = "Seleccionar Carpeta"
$btnSelectFolder.Dock = [System.Windows.Forms.DockStyle]::Top
$btnSelectFolder.Add_Click({
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowser.Description = "Seleccione la carpeta raíz"
    $folderBrowser.RootFolder = [System.Environment+SpecialFolder]::MyComputer

    if ($folderBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $treeView.Nodes.Clear()
        Get-FolderContent -FolderPath $folderBrowser.SelectedPath -TreeView $treeView
        $statusLabel.Text = "Carpeta cargada: $($folderBrowser.SelectedPath)"
    }
})

# Crear la barra de estado
$statusBar = New-Object System.Windows.Forms.StatusStrip
$statusLabel = New-Object System.Windows.Forms.ToolStripStatusLabel
$statusBar.Items.Add($statusLabel)

# Agregar controles al formulario
$form.Controls.Add($treeView)
$form.Controls.Add($btnSelectFolder)
$form.Controls.Add($searchPanel)
$form.Controls.Add($detailsPanel)
$form.Controls.Add($statusBar)

# Mostrar el formulario
$form.ShowDialog()