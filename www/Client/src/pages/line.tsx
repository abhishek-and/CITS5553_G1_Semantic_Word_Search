import LineChart from "~/components/chart/line";

import data from "public/response.json";
import CardList from "~/components/cardlist";
import { Fragment, useRef, useState } from "react";

const Line = () => {
  const list = data.documents;

  const listRef = useRef<HTMLDivElement[]>([]);

  const handleClick = (id: number) => {
    listRef.current[id]?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center self-start">
      <LineChart
        className="sticky top-0 z-50 w-full"
        data={list}
        handleClick={handleClick}
      />
      <div className="flex w-full max-w-3xl flex-col gap-4 pt-32">
        {list.map((doc, idx) => (
          <div ref={(ref: HTMLDivElement) => (listRef.current[idx] = ref)}>
            <CardList doc={doc} key={idx} />
          </div>
        ))}
      </div>
    </main>
  );
};

export default Line;
