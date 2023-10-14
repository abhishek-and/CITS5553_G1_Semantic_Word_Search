import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";

const CardList = ({ doc }: any) => {
  console.log(doc);
  return (
    <Card className="w-full transform rounded-lg border border-gray-300 bg-white shadow-md transition duration-500 ease-in-out hover:scale-105 hover:shadow-lg">
      <CardHeader>
        <CardTitle>{doc.contract_title}</CardTitle>
        {/* <CardDescription>Card Description</CardDescription> */}
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-600">
          Document ID #: {doc.reference_number}
        </p>
        <p className="text-sm text-gray-600">
          Similarity Score: {doc.similarity_score}
        </p>
        <p className="text-sm text-gray-600">Supplier: {doc.supplier_name}</p>
        {/* <p className="text-sm text-gray-600">
UNSPSC Code: {doc["UNSPSC Code"]}
</p> */}
      </CardContent>
      <CardFooter>
        <p>{doc.sentence_piece}</p>
      </CardFooter>
    </Card>
  );
};

export default CardList;
