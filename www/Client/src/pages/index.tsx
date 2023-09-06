import Head from "next/head";
import Data from "./mock-data.json";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    // Implement your search functionality here
    // You can filter the data based on the query
    // For now, let's just log the query
    console.log("Searching for:", query);
  };

  return (
    <>
      <Head>
        <title>Semantic Word Search</title>
        <meta name="description" content="" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="min-h-screen bg-white text-gray-900">
        <div className="container mx-auto flex flex-col items-center p-8">
          <div className="relative mb-4 w-full max-w-3xl">
            <input
              placeholder="Enter search query"
              onChange={(event) => setQuery(event.target.value)}
              className="w-full rounded-full border border-gray-300 bg-gray-100 px-4 py-2 pr-16 text-gray-800"
            />
            <button
              className="absolute right-0 top-0 h-full w-16 rounded-full rounded-l-none bg-blue-500 text-white"
              onClick={handleSearch}
            >
              Search
            </button>
          </div>
          <div className="w-full max-w-3xl">
            {Data.filter((post) => {
              if (query === "") {
                return post;
              } else if (
                post.title.toLowerCase().includes(query.toLowerCase())
              ) {
                return post;
              }
            }).map((post, index) => (
              <div
                className="mb-4 rounded-lg border border-gray-300 bg-white p-6 shadow-md"
                key={index}
              >
                <p className="text-xl font-semibold">{post.title}</p>
                <p className="text-sm text-gray-600">
                  Reference #: {post["Reference #"]}
                </p>
                <p className="text-sm text-gray-600">
                  Close Date: {post["Close Date"]}
                </p>
                <p className="text-sm text-gray-600">
                  UNSPSC Code: {post["UNSPSC Code"]}
                </p>
                {/* Add more fields as needed */}
              </div>
            ))}
          </div>
        </div>
      </main>
    </>
  );
}
