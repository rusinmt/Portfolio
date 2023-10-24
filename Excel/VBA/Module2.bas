Attribute VB_Name = "Module2"
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
