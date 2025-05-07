import React, { useEffect, useRef } from "react";
import Plotly from "plotly.js-dist-min";

interface Chart {
  type: "bar" | "line" | "pie";
  title: string;
  x: any[];
  y: any[];
}

interface ChartsDisplayProps {
  charts: Chart[];
}

const ChartsDisplay: React.FC<ChartsDisplayProps> = ({ charts }) => {
  const containerRefs = useRef<(HTMLDivElement | null)[]>([]);

  useEffect(() => {
    charts.forEach((chart, index) => {
      const container = containerRefs.current[index];
      if (!container) return;

      const plotData =
        chart.type === "pie"
          ? [{ labels: chart.x, values: chart.y, type: chart.type }]
          : [{ x: chart.x, y: chart.y, type: chart.type }];

      const layout = {
        title: chart.title,
        autosize: true,
        margin: { t: 40, l: 40, r: 20, b: 40 }
      };

      Plotly.newPlot(container, plotData, layout, { responsive: true });
    });
  }, [charts]);

  return (
    <div className="mt-8 grid gap-6 grid-cols-1 md:grid-cols-2">
      {charts.map((_, index) => (
        <div
          key={index}
          ref={(el) => (containerRefs.current[index] = el)}
          className="rounded-lg border p-4 bg-white shadow-md"
          style={{ minHeight: "350px" }}
        />
      ))}
    </div>
  );
};

export default ChartsDisplay;
