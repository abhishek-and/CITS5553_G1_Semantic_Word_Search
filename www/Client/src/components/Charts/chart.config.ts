class ChartConfig {
    static get ColumnChartConfig() {
        return {
            chart: {
                type: "bar",
                height: "auto",
                fontFamily: "Poppins",
                toolbar: {
                    show: false,
                    offsetX: 0,
                    offsetY: -35,
                },
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    distributed: true,
                    columnWidth: "55%",
                    endingShape: "rounded",
                },
            },
            dataLabels: {
                enabled: false,
            },
            stroke: {
                show: true,
                width: 2,
                colors: ["transparent"],
            },
            fill: {
                opacity: 1,
            },
        };
    }
    static get ColumnStackedChartConfig() {
        return {
            chart: {
                type: "bar",
                height: "auto",
                fontFamily: "Poppins",
                stacked: true,
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: "55%",
                    endingShape: "rounded",
                },
            },
            dataLabels: {
                enabled: false,
            },
            stroke: {
                show: true,
                width: 2,
                colors: ["transparent"],
            },
            fill: {
                opacity: 1,
            },
        };
    }
    static get PieChartConfig() {
        return {
            chart: {
                width: 200,
                type: "pie",
            },
            responsive: [
                {
                    breakpoint: 1921,
                    options: {
                        chart: {
                            width: 450,
                        },
                        legend: {
                            position: "bottom",
                        },
                    },
                },
                {
                    breakpoint: 1377,
                    options: {
                        chart: {
                            width: 400,
                        },
                        legend: {
                            position: "bottom",
                        },
                    },
                },
                {
                    breakpoint: 920,
                    options: {
                        chart: {
                            width: 300,
                        },
                        legend: {
                            position: "bottom",
                        },
                    },
                },
                {
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 200,
                        },
                        legend: {
                            position: "bottom",
                        },
                    },
                },
            ],
        };
    }
    static get AreaSplineChartConfig() {
        return {
            chart: {
                height: 350,
                type: "area",
                toolbar: {
                    show: false,
                },
            },
            legend: {
                show: true,
                position: "bottom",
            },
            dataLabels: {
                enabled: false,
            },
            stroke: {
                curve: "smooth",
            },
            xaxis: {
                labels: {
                    show: true, 
                },
            },
        };
    }
    static get SemiDonutChartConfig() {
        return {
            chart: {
                height: 350,
                type: "donut",
                toolbar: {
                    show: false,
                },
            },
            legend: {
                position: "bottom",
            },
            dataLabels: {
                enabled: true,
                style: {
                    fontSize: "14px",
                    fontWeight: "normal",
                    colors: undefined,
                },
                background: {
                    enabled: true,
                    foreColor: "#fff",
                    padding: 0,
                    borderRadius: 0,
                    borderWidth: 0,
                    dropShadow: {
                        enabled: false,
                    },
                },
                dropShadow: {
                    enabled: false,
                    top: 1,
                    left: 1,
                    blur: 1,
                    color: "#000",
                    opacity: 0.45,
                },
            },
            responsive: [
                {
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 200,
                        },
                        legend: {
                            position: "top",
                        },
                    },
                },
            ],
        };
    }
}
export default ChartConfig;
