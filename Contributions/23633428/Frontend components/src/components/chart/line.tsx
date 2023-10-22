import {
  Card,
  Title,
  LineChart as Line,
  LineChartProps as LineProps,
} from "@tremor/react";
import { cn } from "~/lib/utils";

interface document {
  client_agency: string;
  contract_title: string;
  procurement_method: string;
  reference_number: string;
  revised_contract_value: number;
  supplier_name: string;
  tender_closing_date: string;
  type_of_work: string;
  unspsc_code: number;
  unspsc_title: string;
  similarity_score: number;
  sentence_piece: string;
  row_id: string;
}

interface LineChartProps {
  data: document[];
  className?: string;
  handleClick?: (id: number) => void;
}

type CustomTooltip = LineProps["customTooltip"];

const customTooltip: CustomTooltip = ({ payload, active }) => {
  if (!active || !payload) return null;
  return (
    <div className="mt-80 w-80 rounded-tremor-default border border-tremor-border bg-tremor-background p-2 text-tremor-default shadow-tremor-dropdown">
      {payload.length >= 1 && (
        <div className="flex flex-1 space-x-2.5">
          <div
            className={`flex w-auto flex-col bg-${payload[0]?.color}-500 rounded`}
          />
          <div className="space-y-1">
            <p className="text-tremor-content">Similarity Score</p>
            <p className="font-medium text-tremor-content-emphasis">
              {Math.round(Number(payload[0]?.value) * 10000) / 10000}
            </p>
            <p className="text-tremor-content">Total Contracts</p>
            <p className="font-medium text-tremor-content-emphasis">
              {Number(payload[0]?.payload.row_id) + 1}
            </p>
            <p className="text-tremor-content">Reference Number</p>
            <p className="font-medium text-tremor-content-emphasis">
              {payload[0]?.payload.reference_number}
            </p>
            <p className="text-tremor-content">Contract Title</p>
            <p className="font-medium text-tremor-content-emphasis">
              {payload[0]?.payload.contract_title}
            </p>
            <p className="text-tremor-content">Sentence Piece</p>
            <p className="font-medium text-tremor-content-emphasis">
              {payload[0]?.payload.sentence_piece}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

const LineChart = ({ data, className, handleClick }: LineChartProps) => {
  const indexedData = data.map((doc, idx) => ({ ...doc, idx }));

  return (
    <Card className={cn(className)}>
      <Title>Similarity Line Chart</Title>
      <Line
        className="mt-6"
        data={indexedData}
        index="row_id"
        categories={["similarity_score"]}
        colors={["blue"]}
        yAxisWidth={40}
        customTooltip={customTooltip}
        showAnimation
        onValueChange={(v) => handleClick?.(Number(v?.idx))}
      />
    </Card>
  );
};

export default LineChart;
