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
import { Chart } from "react-charts";
import AreaSplineChart from "../Charts/AreaCharts/AreaSplineChart";
// import { ChartComponent } from "./charts";

export const ViewDocument = (props: any) => {
  const { open, onClose, documentcontent, semanticScoreData } = props;
  console.log(semanticScoreData?.data?.semantic_scores);
  console.log(semanticScoreData?.data?.words);
  const [scroll, setScroll] = React.useState("paper");

  return (
    <React.Fragment>
      <Dialog onClose={onClose} open={open} fullWidth={true} maxWidth={"xl"}>
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

          <div className="ju mx-auto flex max-w-6xl flex-col items-center justify-center pt-6">
            <div className="pb-4 text-center text-xl font-bold">
              Semantic Similar Words
            </div>

            <table className="table-auto border-collapse rounded-md border border-slate-800">
              <thead>
                <tr>
                  <th className="w-[20%] border border-slate-800 p-1">Words</th>
                  <th className="w-[20%] border border-slate-800 p-1">
                    Similarity Score
                  </th>
                </tr>
              </thead>
              <tbody>
                {semanticScoreData?.data?.words
                  .map((word: any, index: any) => ({
                    word,
                    score: semanticScoreData?.data?.semantic_scores[index],
                  }))
                  .sort((a: any, b: any) => b.score - a.score) // Sort by score in descending order
                  .map((item: any, index: any) => (
                    <tr key={index} className="">
                      <td className="border border-slate-800 p-1 text-center">
                        {item.word}
                      </td>
                      <td className="text-cn border border-slate-800 p-1 text-center">
                        {(item.score * 100).toFixed(2)}%
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
          <div>
            {/* <AreaSplineChart
              data={semanticScoreData?.data?.words}
              options={semanticScoreData?.data?.semantic_scores}
              height={300}
            /> */}
          </div>
        </DialogContent>
      </Dialog>
    </React.Fragment>
  );
};
