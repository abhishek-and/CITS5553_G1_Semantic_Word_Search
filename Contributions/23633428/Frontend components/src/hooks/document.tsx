import {
  MutationFunction,
  UseMutationOptions,
  useMutation,
} from "@tanstack/react-query";
import axios from "axios";

interface Document {
  documentName: string;
  documentID: string;
  similarityScore: string;
}

type QueryData = {
  documents: Document[];
};
type QueryVariables = {
  query: any;
  start_date: string;
  end_date: string;
};

const useMutationDocuments = (
  options: UseMutationOptions<QueryData, unknown, QueryVariables>,
) => {
  const mutationFn: MutationFunction<QueryData, QueryVariables> = async (
    query,
  ) => {
    const { data: response } = await axios.post(
      "http://127.0.0.1:8000/api/getDocuments",
      query,
    );
    return response;
  };
  return useMutation({ ...options, mutationFn });
};

export default useMutationDocuments;
