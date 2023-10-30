[void][System.Reflection.Assembly]::LoadWithPartialName("PresentationFramework")

$window = New-Object Windows.Window

$window.Width = 1200
$window.Height = 900
$window.Title = "Listar Archivos y Carpetas"

$label = New-Object Windows.Controls.Label
$label.Content = "Ingrese el nombre de la carpeta que desea listar:"
$label.Width = 380
$label.Margin = "10,10,0,0"

$textBox = New-Object Windows.Controls.TextBox
$textBox.Width = 300
$textBox.Margin = "10,30,0,0"

$button = New-Object Windows.Controls.Button
$button.Content = "Listar"
$button.Margin = "10,60,0,0"

$resultTextBox = New-Object Windows.Controls.TextBox
$resultTextBox.Width = 380
$resultTextBox.Height = 150
$resultTextBox.AcceptsReturn = $true
$resultTextBox.Margin = "10,90,0,0"
$resultTextBox.IsReadOnly = $true

$button.Add_Click({
    $nombreCarpeta = $textBox.Text

    # Obtener la ubicación del script actual
    $scriptPath = "C:\Users\APM01-53\Documents\Sicer\Repos\Scripts\Etica\Ps1\VerArchivos\ArchivosVS5.ps1"

    if (Test-Path $scriptPath) {
        $resultado = & $scriptPath -nombreCarpeta $nombreCarpeta
        $resultTextBox.Text = $resultado
    } else {
        $resultTextBox.Text = "El archivo 'TuScript.ps1' no se encuentra en la ubicación correcta."
    }
})

$window.Content = [Windows.Controls.StackPanel]::new()
$window.Content.Children.Add($label)
$window.Content.Children.Add($textBox)
$window.Content.Children.Add($button)
$window.Content.Children.Add($resultTextBox)

$window.ShowDialog()
