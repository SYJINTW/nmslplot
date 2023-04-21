import nmslplot
import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    csvFilePath = Path("sample_data")/"data_with_hue.csv"
    df = pd.read_csv(csvFilePath)

    saveFigDir = Path("figs")
    saveFigDir.mkdir(parents=True, exist_ok=True)

    # barplot without hue, Y is Value1 (just X and Y)
    nmslplot.nmslBarPlot(
            df=df, 
            x="Category", y="Value1",
            xlim = "", ylim = "", 
            xlabel = "X Label", ylabel = "Y Label", 
            loc='lower left', 
            savePlot = True, showPlot = False,
            saveDir = saveFigDir, saveImgName = "without_hue_value1"
            )

    # barplot with hue, Y is Value1
    nmslplot.nmslBarPlot(
            df=df, 
            x="Category", y="Value1", hue="Hue", 
            xlim = "", ylim = "", 
            xlabel = "X Label", ylabel = "Y Label", 
            loc='lower left', 
            savePlot = True, showPlot = False,
            saveDir = saveFigDir, saveImgName = "with_hue_value1"
            )

    # barplot with hue, Y is Value2
    nmslplot.nmslBarPlot(
            df=df, 
            x="Category", y="Value2", hue="Hue",
            xlim = "", ylim = "", 
            xlabel = "X Label", ylabel = "Y Label", 
            loc='lower left', 
            savePlot = True, showPlot = False,
            saveDir = saveFigDir, saveImgName = "with_hue_value2"
            )