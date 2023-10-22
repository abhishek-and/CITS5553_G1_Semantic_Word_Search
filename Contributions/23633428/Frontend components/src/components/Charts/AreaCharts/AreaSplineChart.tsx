import Chart from "react-apexcharts";
import ChartConfig from "../chart.config";
import { useEffect, useState } from "react";

interface AreaSplineChartProps {
  data: any[];
  options: any;
  height?: number | string;
  width?: number | string;
}
const AreaSplineChart = ({
  data,
  options,
  height,
  width,
}: AreaSplineChartProps) => {
  useEffect(() => {
    if (options && data) {
      setChartData({
        options: {
          ...ChartConfig.AreaSplineChartConfig,
          ...(options ?? {}),
        },
        data,
      });
    }
  }, [options, data]);
  const [chartData, setChartData] = useState<AreaSplineChartProps>({
    data: [],
    options: {},
  });
  return (
    <Chart
      type="area"
      options={chartData.options}
      series={chartData.data}
      height={height}
      width={width}
    />
  );
};
export default AreaSplineChart;
