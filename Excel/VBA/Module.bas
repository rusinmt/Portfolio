Attribute VB_Name = "Module1"
Sub Clear()
Attribute Clear.VB_ProcData.VB_Invoke_Func = " \n14"

    ActiveWorkbook.SlicerCaches("Slicer_County").ClearManualFilter
    ActiveWorkbook.SlicerCaches("Slicer_Make").ClearManualFilter
    ActiveWorkbook.SlicerCaches("Slicer_Model").ClearManualFilter

End Sub

Sub DropDown()
    
    With ActiveWorkbook.SlicerCaches("Slicer_Fuel_Type1")
        If Range("U13").Value = "1" Then
            .SlicerItems("Electric Chargers").Selected = True
            .SlicerItems("Hydrogen Fueling Stations").Selected = False
        ElseIf Range("U13").Value = "2" Then
            .ClearManualFilter
            .SlicerItems("Electric Chargers").Selected = False
            .SlicerItems("Hydrogen Fueling Stations").Selected = True
        End If
    End With
    
End Sub
