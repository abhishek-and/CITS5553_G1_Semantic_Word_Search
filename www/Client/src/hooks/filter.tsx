import {
  MutationFunction,
  UseMutationOptions,
  useMutation,
} from "@tanstack/react-query";
import axios from "axios";

type QueryData = {
  query: string;
  start_date: string;
  end_date: string;
};
type QueryVariables = string;

const useMutationFilters = (
  options: UseMutationOptions<QueryData, unknown, QueryVariables>,
) => {
  const mutationFn: MutationFunction<QueryData, QueryVariables> = async (
    query,
  ) => {
    const { data: response } = await axios.post(
      "http://127.0.0.1:8000/api/getFilters",
      { query },
    );
    return response;
  };
  return useMutation({ ...options, mutationFn });
};

export default useMutationFilters;
