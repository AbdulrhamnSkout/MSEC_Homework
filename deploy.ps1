
New-AzResourceGroup -Name 'abd-arm3' -Location "Central US"

New-AzResourceGroupDeployment `
  -Name 'test' `
  -ResourceGroupName 'abd-arm3' `
  -TemplateFile 'storageAccount.json'

New-AzResourceGroupDeployment `
  -Name 'test1' `
  -ResourceGroupName 'abd-arm3' `
  -TemplateFile 'vm.json'