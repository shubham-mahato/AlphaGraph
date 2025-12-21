"use client";
import { useState } from "react";

type Props = {
  onSearch: (ticker: string) => void;
};

export default function SearchBar({ onSearch }: Props) {
  const [ticker, setTicker] = useState("TCS");

  return (
    <div className="flex gap-2 mb-6">
      <input
        className="border border-gray-300 rounded-md px-4 py-2 w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={ticker}
        onChange={(e) => setTicker(e.target.value.toUpperCase())}
        placeholder="Enter Ticker (e.g. TCS)"
        onKeyDown={(e) => e.key === "Enter" && onSearch(ticker)}
      />
      <button 
        onClick={() => onSearch(ticker)}
        className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors"
      >
        Analyze
      </button>
    </div>
  );
}