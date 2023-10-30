import {
  Button,
  Dialog,
  DialogContent,
  DialogTitle,
  IconButton,
  Box,
  Tab,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import PixOutlinedIcon from "@mui/icons-material/PixOutlined";
import CloseIcon from "@mui/icons-material/Close";
import Loader from "react-loader";
import AreaSplineChart from "../Charts/AreaCharts/AreaSplineChart";
import moment from "moment";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
// import { ChartComponent } from "./charts";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

export const ViewDocument = (props: any) => {
  const { open, onClose, documentcontent, semanticScoreData } = props;
  console.log(props);
  const [loaded, setLoaded] = useState(true);
  const [browserloader, setBrowserLoaded] = useState(true);
  console.log(semanticScoreData?.data?.semantic_scores);
  console.log(semanticScoreData?.data?.words);
  const [scroll, setScroll] = React.useState("paper");

  useEffect(() => {
    console.log(semanticScoreData?.data?.semantic_scores?.length);
    if (semanticScoreData?.data?.semantic_scores?.length > 0) {
      setBrowserLoaded(true);
      setLoaded(true);
    } else {
      setLoaded(false);
      setBrowserLoaded(false);
    }
  }, [semanticScoreData?.data]);

  const handleClose = () => {
    onClose(true);
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: "Semantic Similar Word Score",
      },
    },
    scales: {
      y: {
        max: 100,
        min: 60,
        stepSize: 10,
        ticks: {
          stepSize: 10,
        },
      },
    },
  };

  const semanticScores = semanticScoreData?.data?.semantic_scores;
  const words = semanticScoreData?.data?.words;

  // Create an array of objects containing words and their corresponding scores
  const scoreWordPairs = semanticScores?.map((score: any, index: any) => ({
    score: score * 100,
    word: words?.[index] || "", // Use an empty string if word is undefined
  }));

  scoreWordPairs?.sort((a: any, b: any) => b.score - a.score);

  // Extract the sorted words and sorted percentages
  const sortedWords = scoreWordPairs?.map((pair: any) => pair.word);
  const sortedPercentages = scoreWordPairs?.map((pair: any) => pair.score);

  const data = {
    labels: sortedWords,
    datasets: [
      {
        label: "",
        data: sortedPercentages,
        backgroundColor: "#3B82F6",
        barThickness: 20,
      },
    ],
  };

  return (
    <React.Fragment>
      <Dialog
        onClose={() => handleClose()}
        open={open}
        fullWidth={true}
        maxWidth={"xl"}
        className="h-full"
      >
        <DialogTitle sx={{ m: 0, p: 2 }} className="">
          <h4 className="text-lg font-semibold">
            {documentcontent?.contract_title}
          </h4>
          <IconButton
            aria-label="close"
            className="head-close-bttn"
            onClick={() => onClose(true)}
            sx={{
              position: "absolute",
              right: 8,
              top: 8,
              color: (theme) => theme.palette.grey[500],
            }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>

        <DialogContent dividers={scroll === "paper"}>
          <div className="h-[38rem]">
            {browserloader ? (
              <>
                <div className="flex gap-2">
                  <div>
                    <div>
                      Client Agency:{" "}
                      <span className="text-lg font-bold">
                        {documentcontent?.client_agency}
                      </span>
                    </div>
                    <div>
                      Supplier Name:{" "}
                      <span className="text-lg font-bold">
                        {documentcontent?.supplier_name}
                      </span>
                    </div>
                    <div>
                      Reference Number:{" "}
                      <span className="text-lg font-bold">
                        {documentcontent?.reference_number}
                      </span>
                    </div>
                  </div>
                  <div>
                    <div className="pt-8">
                      UNSPSC Code:{" "}
                      <span className="text-lg font-bold">
                        {documentcontent?.unspsc_code}
                      </span>
                    </div>
                    <div>
                      UNSPSC Title:{" "}
                      <span className="text-lg font-bold">
                        {documentcontent?.unspsc_title}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="h-[25rem]">
                  <div className="flex h-full w-full flex-col items-center justify-center pb-8 pt-6">
                    <Bar options={options} data={data} />
                  </div>
                </div>
              </>
            ) : (
              <Loader
                loaded={loaded}
                lines={13}
                length={25}
                width={9}
                radius={35}
                corners={1}
                rotate={0}
                direction={1}
                color="#3B82F6"
                speed={1}
                trail={60}
                shadow={true}
                hwaccel={false}
                className="spinner"
                zIndex={2e9}
                top="50%"
                left="50%"
                scale={1.0}
                loadedClassName="loadedContent"
              />
            )}
          </div>
        </DialogContent>
      </Dialog>
    </React.Fragment>
  );
};
