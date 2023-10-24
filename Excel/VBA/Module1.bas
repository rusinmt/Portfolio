Attribute VB_Name = "Module1"
Sub Clear()

    ActiveWorkbook.SlicerCaches("Slicer_County").ClearManualFilter
    ActiveWorkbook.SlicerCaches("Slicer_Make").ClearManualFilter
    ActiveWorkbook.SlicerCaches("Slicer_Model").ClearManualFilter

End Sub

