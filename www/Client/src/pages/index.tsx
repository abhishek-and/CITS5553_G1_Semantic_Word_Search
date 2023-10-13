import Head from "next/head";
import Data from "./mock-data.json";
import { useState } from "react";
import Image from "next/image";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

import { Button } from "~/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormInputDate,
  FormItem,
  FormLabel,
  FormMessage,
} from "~/components/ui/form";
import { Input } from "~/components/ui/input";
import { Controller, useForm } from "react-hook-form";
import useMutationFilters from "~/hooks/filter";
import useMutationDocuments from "~/hooks/document";
import { Slider } from "@mui/material";
import { Checkbox, FormControlLabel, Radio, RadioGroup } from "@mui/material";
import axios from "axios";
import CardList from "~/components/cardlist";

const formSchema = z.object({
  query: z.string().min(0, {
    // message: "query must be at least 2 characters.",
  }),
  startDate: z.any(),
  endDate: z.any(),
  Range: z.any(),
  typeOfWork: z.any(),
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
  const [values, setValue] = useState<any>();
  const [res, sethandleResponse] = useState<any>();

  const { mutateAsync: mutateFilters, isSuccess: isSuccessFilters } =
    useMutationFilters({
      onSuccess: (data: any) => console.log(data),
      onError: (error: any) => console.error(error),
    });
  const { mutateAsync: mutateDocuments } = useMutationDocuments({
    onSuccess: (data: any) => console.log(data),
    onError: (error: any) => console.error(error),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      query: "",
    },
  });

  // 2. Define a submit handler.
  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    const { query, startDate, endDate, ...restOfValues } = values;
    // console.log(query.toString());
    // const filtersTemp = await mutateFilters(JSON.stringify(values));
    // const documentsTemp = await mutateDocuments(filtersTemp);
    // setFilters(filtersTemp);
    // setDocuemnts(documentsTemp.documents);
    // setValue(documentsTemp.documents);
    // sethandleResponse(JSON.stringify(values));

    const payload = {
      query: JSON.stringify({ query: values.query }),
    };
    const { data: response } = await axios.post(
      "http://127.0.0.1:8000/api/getFilters",
      payload,
    );
    const { start_date, end_date, ...rest } = response;

    const docpayload = {
      start_date: values.startDate || start_date,
      end_date: values.endDate || end_date,
      ...rest,
      ...restOfValues,
    };

    console.log(docpayload);

    const { data: docresponse } = await axios.post(
      "http://127.0.0.1:8000/api/getDocuments",
      docpayload,
    );
    setDocuemnts(docresponse.documents);
    setValue(docresponse.documents);
  };

  console.log(values);

  const clearList = () => {
    setValue([]);
  };

  const [value, setValues] = useState<number[]>([0, 5000]);

  const handleChange = (event: Event, newValue: number | number[]) => {
    setValues(newValue as number[]);
  };

  function valuetext(value: number) {
    return `${value}°C`;
  }

  const config = { label: "label", value: "value" };

  const fruitOptions = [
    {
      label: "Works",
      value: 1,
    },
    {
      label: "Goods and Services",
      value: 2,
    },
  ];

  const test = () => {
    console.log(form.formState.errors);
  };

  return (
    <>
      <Head>
        <title>Semantic Word Search</title>
        <meta name="description" content="" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="flex min-h-screen flex-col items-center justify-center bg-white text-gray-900">
        <div className="flex w-full items-center justify-center p-8">
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="mb-4 flex w-full items-start justify-center gap-32"
            >
              <div className="flex w-[18%] flex-col gap-6">
                <div className="flex items-center gap-2">
                  <div className="text-3xl font-semibold text-black">
                    Filters
                  </div>
                  <Image
                    src="/static/assets/filter.svg"
                    alt="ITC logo"
                    width={30}
                    height={30}
                  />
                </div>
                <div className="rounded-md border border-gray-300 px-4 pb-4 pt-2 drop-shadow-xl">
                  <FormLabel className="text-lg">Type of Work</FormLabel>
                  <div className="p-1"></div>
                  <Controller
                    rules={{ required: true }}
                    control={form.control}
                    name="typeOfWork"
                    render={({ field }) => {
                      return (
                        <RadioGroup {...field}>
                          <FormControlLabel
                            value="Works"
                            control={<Radio />}
                            label="Works"
                          />
                          <FormControlLabel
                            value="Goods and Services"
                            control={<Radio />}
                            label="Goods and Services"
                          />
                        </RadioGroup>
                      );
                    }}
                  />
                </div>
                <div className="rounded-md border border-gray-300 px-4 pb-4 pt-2 drop-shadow-xl">
                  <FormLabel className="text-lg">Date Picker</FormLabel>
                  <div className="p-1 pb-2"></div>
                  <FormInputDate
                    name="startDate"
                    control={form.control}
                    label="Start Date"
                    inputFormat="DD/MM/YYYY"
                    onChange={(date: any) => {
                      console.log(date);
                    }}
                  />
                  <div className="p-3"></div>
                  {/* <FormLabel>End Date</FormLabel> */}
                  <FormInputDate
                    name="endDate"
                    control={form.control}
                    label="End Date"
                    inputFormat="DD/MM/YYYY"
                    onChange={(date: any) => {
                      console.log(date);
                    }}
                  />
                </div>
                {/* <div className="p-1"></div> */}
                <div className="rounded-md border border-gray-300 px-4 pb-4 pt-2 drop-shadow-xl">
                  <FormLabel className="text-lg">Price Range ($)</FormLabel>
                  <div className="p-6"></div>
                  <Controller
                    name="Range"
                    control={form.control}
                    render={({ field }) => (
                      <Slider
                        getAriaLabel={() => "Temperature range"}
                        value={value}
                        onChange={(event, newValue) => {
                          handleChange(event, newValue);
                          field.onChange(newValue); // Update the form field value
                        }}
                        valueLabelDisplay="on"
                        getAriaValueText={valuetext}
                        step={100}
                        min={0}
                        max={5000}
                      />
                    )}
                  />
                </div>
              </div>

              <div className="relative w-[45%]">
                <div className="w-full">
                  <FormField
                    control={form.control}
                    name="query"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-lg">
                          Enter search query
                        </FormLabel>
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
                  <Image
                    src="/static/assets/close_btn.svg"
                    alt="ITC logo"
                    width={40}
                    height={40}
                    className="absolute right-[70px] top-[2.25rem]"
                    onClick={() => clearList()}
                  />
                  <Button
                    className="absolute right-0 top-[2.25rem] h-10 w-16 rounded-full rounded-l-none bg-blue-500 text-white"
                    type="submit"
                  >
                    Submit
                  </Button>
                  <div className="flex h-screen w-full max-w-3xl flex-col gap-4 pt-3">
                    {values?.length > 0 &&
                      values.map((doc: any) => (
                        <CardList doc={doc} key={doc.id} />
                      ))}
                  </div>
                </div>
              </div>
            </form>
          </Form>
        </div>
      </main>
    </>
  );
}
