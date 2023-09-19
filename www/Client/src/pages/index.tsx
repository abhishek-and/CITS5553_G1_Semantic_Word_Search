import Head from "next/head";
import Data from "./mock-data.json";
import { useState } from "react";

import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

import { Button } from "~/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "~/components/ui/form";
import { Input } from "~/components/ui/input";
import { useForm } from "react-hook-form";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";
import useMutationFilters from "~/hooks/filter";
import useMutationDocuments from "~/hooks/document";

const formSchema = z.object({
  query: z.string().min(0, {
    // message: "query must be at least 2 characters.",
  }),
});

const mockDataSchema = z.object({
  id: z.number(),
  title: z.string(),
  "Reference #": z.string(),
  "Close Date": z.string(),
  "UNSPSC Code": z.number(),
});

const mockDataArraySchema = z.array(mockDataSchema);

const docsData = mockDataArraySchema.parse(Data);

export default function Home() {
  const [docs, setDocs] = useState(docsData);
  const [filters, setFilters] = useState({});
  const [documents, setDocuemnts] = useState({});

  const { mutateAsync: mutateFilters, isSuccess: isSuccessFilters } =
    useMutationFilters({
      onSuccess: (data) => console.log(data),
      onError: (error) => console.error(error),
    });
  const { mutateAsync: mutateDocuments } = useMutationDocuments({
    onSuccess: (data) => console.log(data),
    onError: (error) => console.error(error),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      query: "",
    },
  });

  // 2. Define a submit handler.
  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    const filtersTemp = await mutateFilters(values.query);
    const documentsTemp = await mutateDocuments(filtersTemp);
    setFilters(filtersTemp);
    setDocuemnts(documentsTemp);
    const results = Data.filter((item) =>
      item.title.toLowerCase().includes(values.query.toLowerCase()),
    );
    setDocs(results);
  };

  return (
    <>
      <Head>
        <title>Semantic Word Search</title>
        <meta name="description" content="" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="flex min-h-screen flex-col items-center justify-center bg-white text-gray-900">
        <div className="container mx-auto flex flex-col items-center p-8">
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="relative mb-4 w-full max-w-3xl"
            >
              <FormField
                control={form.control}
                name="query"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Enter search query</FormLabel>
                    <FormControl>
                      <Input
                        className="w-full rounded-full border border-gray-300 bg-gray-100 px-4 py-2 pr-16 text-gray-800"
                        placeholder="CCTV from 13 Dec 2017 to 13 Jan 2019"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button
                className="absolute right-0 top-8 h-10 w-16 rounded-full rounded-l-none bg-blue-500 text-white"
                type="submit"
              >
                Submit
              </Button>
            </form>
          </Form>
          <div>
            <pre>{JSON.stringify(filters, null, 2)}</pre>
          </div>
          <div>
            <pre>{JSON.stringify(documents, null, 2)}</pre>
          </div>
          <div className="flex w-full max-w-3xl flex-col gap-4">
            {docs.length > 0 &&
              docs.map((doc) => (
                <Card
                  key={doc.id}
                  className="transform rounded-lg border border-gray-300 bg-white shadow-md transition duration-500 ease-in-out hover:scale-105 hover:shadow-lg"
                >
                  <CardHeader>
                    <CardTitle>{doc.title}</CardTitle>
                    {/* <CardDescription>Card Description</CardDescription> */}
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600">
                      Reference #: {doc["Reference #"]}
                    </p>
                    <p className="text-sm text-gray-600">
                      Close Date: {doc["Close Date"]}
                    </p>
                    <p className="text-sm text-gray-600">
                      UNSPSC Code: {doc["UNSPSC Code"]}
                    </p>
                  </CardContent>
                  {/* <CardFooter>
                    <p>Card Footer</p>
                  </CardFooter> */}
                </Card>
              ))}
          </div>
        </div>
      </main>
    </>
  );
}
