## Popularity of Hydrogen-Powered Vehicles compared to Electric in California

Analyzing the adoption of hydrogen-powered vehicles and comparing their prevalence to electric vehicles, this project aims to offer valuable insights into the state's journey towards sustainable mobility. The main focus is on a comprehensive analysis of manufacturer engagement, customer preferences, and infrastructure development. Through a dashboard showcasing data sourced from the California Energy Commission, the project unravels trends, challenges, and opportunities that are shaping the future of transportation in this forward-thinking region. The findings and conclusions are insightful for policymakers in the region who could shape policies and incentives to promote the adoption of fuel cell vehicles in the future. Investors in the clean energy and transportation sectors can make informed decisions based on trends and growth opportunities in the hydrogen vehicle market. Automakers can leverage insights to make informed changes in their strategies and marketing.

## Excel

The portfolio project entailed a comprehensive series of data management and analysis tasks. To begin, Power Query played a pivotal role in appending and transforming the data, ensuring its structure and organization for subsequent analysis. This initial step laid the foundation for a more in-depth exploration of the dataset.

Subsequently, Power Pivot was employed to establish a data model, involving the creation of relationships between different data sets. This phase required a deeper understanding of the queried data to derive meaningful connections and insights. The project delved further into the dataset, implementing advanced functions and techniques, including Find and Replace, Index(Match), SUMIF, and XLOOKUP, to manipulate and extract data effectively.

Handling data in various formats, such as unifying date formats and incorporating geographic data, presented its own set of challenges. The utilization of pivot tables proved invaluable in structuring and summarizing data efficiently. Additionally, conditional data manipulation was achieved through the use of functions like IF() and FILTER(), while custom formatting and DAX measures were used in presenting key metrics in the dashboard.

VBA code automates two funtions of the Dashboard.

```vba
Sub Clear()

    ActiveWorkbook.SlicerCaches("Slicer_County").ClearManualFilter
    ActiveWorkbook.SlicerCaches("Slicer_Make").ClearManualFilter
    ActiveWorkbook.SlicerCaches("Slicer_Model").ClearManualFilter

End Sub
```

First one helps to clear manual filters for "County", "Make" and "Model" slicers while exploaring the data.

```vba
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
```
Another connects the functionality of the Combo Box drop down list, from Form Control elements, used for more user friendly and aestheticly pleasing interface. It uses Cell Link to define which Fuel Type to show on the interactive 'Chart 1.1' by filtering correct values from the Table 'Map' via dedicated slicer.
```vba
ClearManualFilter
```
Line prevented the slicer from 'Multi-Select' of two values at once.

```dax
= DIVIDE([Sum of Number of New Sales];[Sum of Number of Population]; "2010-2022")
```
DAX generates two of the measures from the Dasboard. Ratio of New Sales in the Vehicle Population in percents. The third argument in the function returns note about the data limitation if Population equals 0.
```dax
=[Sum of Number of Population] + CALCULATE('fSales'[Sum of Number of New Sales]; 'fSales'[YearID] = 14)
```
Second measure estimates the Total of the Population using Sum of Population and Sales from 2023.

Year over year differences where automaticly generated using Pivot Table Value Field Settings. 

Custom Formatting used ${\color{red}▼}$ ${\color{green}▲}$ indicators showcasing values to previous year is linked to the dashoard as a Linked Picture using Othe Paste Options.
