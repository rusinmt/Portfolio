## Popularity of Hydrogen-Powered Vehicles compared to Electric in California

Analyzing the adoption of Hydrogen-Powered Vehicles and comparing their prevalence to electric vehicles, this project aims to offer valuable insights into the state's journey towards sustainable mobility. The main focus is on a comprehensive analysis of manufacturer engagement, customer preferences, and infrastructure development. Through a dashboard showcasing data sourced from the California Energy Commission, the project unravels trends, challenges, and opportunities that are shaping the future of transportation in this forward-thinking region. The findings and conclusions are insightful for policymakers in the region who could shape policies and incentives to promote the adoption of fuel cell vehicles in the future. Investors in the clean energy and transportation sectors can make informed decisions based on trends and growth opportunities in the hydrogen vehicle market. Automakers can leverage insights to make informed changes in their strategies and marketing.

## Excel

The portfolio project entailed a comprehensive series of data management and analysis tasks. To begin, Power Query played a pivotal role in appending and transforming the data, ensuring its structure and organization for subsequent analysis. This initial step laid the foundation for a more in-depth exploration of the dataset.

Subsequently, Power Pivot was employed to establish a data model, involving the creation of relationships between data. This phase required a deeper understanding of the queried dataset to derive meaningful connections and insights. 

![datamodel](https://github.com/rusinmt/portfolio/assets/143091357/e67143ee-e4df-4e14-ba0f-20c2b831b28d)

The project delved deeper into the dataset, implementing structured functions such as Find and Replace, Index(Match), SUMIF, and XLOOKUP, to effectively manipulate and extract data.

Managing data in various formats, such as standardizing date formats and incorporating geographic data. The utilization of pivot tables proved invaluable in structuring and summarizing data efficiently. Additionally, conditional data manipulation was achieved through the use of functions like IF() and FILTER(), while custom formatting and DAX measures were used in presenting key metrics in the dashboard.

VBA code automates two funtions of the Dashboard.

```vba
Sub Clear()

    ActiveWorkbook.SlicerCaches("Slicer_County").ClearManualFilter
    ActiveWorkbook.SlicerCaches("Slicer_Make").ClearManualFilter
    ActiveWorkbook.SlicerCaches("Slicer_Model").ClearManualFilter

End Sub
```

The first one helps clear manual filters for 'County,' 'Make,' and 'Model' slicers while exploring the data.

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
Another connects the functionality of the Combo Box drop down list, from Form Control elements, used for more user friendly and aesthetically pleasing interface. It uses Cell Link to define which Fuel Type to show on the interactive 'Chart 1.1' by filtering correct values from the Table 'Map' via dedicated slicer.
```vba
ClearManualFilter
```
Line prevented the slicer from 'Multi-Select' of two values at once.

```dax
= DIVIDE([Sum of Number of New Sales];[Sum of Number of Population]; "2010-2022")
```
DAX generates two of the measures from the Dashboard. Ratio of New Sales in the Vehicle Population in percents. The third argument in the function returns note about the data limitation if Population equals 0.
```dax
=[Sum of Number of Population] + CALCULATE('fSales'[Sum of Number of New Sales]; 'fSales'[YearID] = 14)
```
Second measure estimates the Total of the Population using Sum of Population and Sales from 2023.

Year-Over-Year differences were automatically generated using Pivot Table Value Field Settings. 

Custom Formatting used ${\color{red}▼}$ ${\color{green}▲}$ indicators showcasing values to previous year is linked to the Dashoard as a Linked Picture using Othe Paste Options.

## Analysis

Hydrogen-Powered Vehicles constitute a small fraction compared to electric vehicles, with a ratio of 1 to 59. California benefits from a <br> well-established network of electric vehicle charging stations, which mirrors the distribution of the vehicle population across the state. When we scrutinize the distribution of hydrogen refueling stations, it becomes evident that certain counties are currently underserved in this aspect 

Among major automakers, Toyota stands out as the primary pioneer in hydrogen fuel cell technology within California, partnering with Subaru, Honda, and Hyundai. This unique position signals potential opportunities for other manufacturers to enter this burgeoning domain. The years 2014-2016 stand as a notable period, highlighting the feasibility of venturing into this market. Toyota's introduction of the popular Mirai model in 2015 propelled them to become the sales leader for subsequent years. The Hydrogen-Powered Vehicles market demonstrates significant potential and opportunities, exemplified by Toyota's remarkable sales growth of over 200% from the previous year in 2021. In a comparison with Tesla's performance in the electric vehicle market, which also saw impressive growth at 70% from the previous year. Toyota managed to surpass Tesla in year-over-year percentage values in 2016, outshining EVs manufaturer success from 2013, albeit on a smaller scale. Tesla's sales figures up to year 2016 are in close proximity to Toyota's number at present, indicating that the best for the Fuel Cell vehicles market is yet to come. 

Customer preferences are influenced by the factors mentioned above, including considerations such as refueling convenience, marketing and the popularity of automaker brands. The entry of more automakers into the Hydrogen-Poered Vehicles market could polarize customer choices. In summary, awareness about this technology tends to increase gradually over time. This evolving perspective could potentially accelerate the adoption rate of hydrogen vehicles in California, resulting in an expansion in both the number and scale of fuel cell technology recipients, and further fostering growth in popularity.
