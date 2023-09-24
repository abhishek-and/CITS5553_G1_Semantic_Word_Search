// import Chart from "chart.js/auto";
// import { useRef, useEffect } from "react";
// // import { ChartDataLabels } from "chartjs-plugin-datalabels";

// export default function PieChart({ value }: any) {
//   const canvasRef = useRef(null);

//   useEffect(() => {
//     const ctx = canvasRef.current.getContext("2d");

//     const chart = new Chart(ctx, {
//       type: "pie",
//       data: {
//         labels: ["Slice 1"],
//         datasets: [
//           {
//             data: [value],
//             backgroundColor: ["#FF0000"],
//           },
//         ],
//       },
//       plugins: [
//         new ChartDataLabels({
//           formatter: (value: any) => `${value}%`,
//           inside: true,
//         }),
//       ],
//     });

//     // Update the chart completeness based on the value prop
//     const updateChartCompleteness = () => {
//       chart.config.data.datasets[0].data = [value];
//       chart.update();
//     };

//     updateChartCompleteness();

//     // Return a function to clean up the chart when the component unmounts
//     return () => chart.destroy();
//   }, [canvasRef, value]);

//   return <canvas ref={canvasRef} />;
// }
