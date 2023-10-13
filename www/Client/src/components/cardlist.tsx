import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";

const CardList = (doc: any) => {
  return (
    <Card
      key={doc.id}
      className="w-full transform rounded-lg border border-gray-300 bg-white shadow-md transition duration-500 ease-in-out hover:scale-105 hover:shadow-lg"
    >
      <CardHeader>
        <CardTitle>{doc.documentName}</CardTitle>
        {/* <CardDescription>Card Description</CardDescription> */}
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-600">Document ID #: {doc.documentID}</p>
        <p className="text-sm text-gray-600">
          Similarity Score: {doc.similarityScore}
        </p>
        {/* <p className="text-sm text-gray-600">
UNSPSC Code: {doc["UNSPSC Code"]}
</p> */}
      </CardContent>
      {/* <CardFooter>
<p>Card Footer</p>
</CardFooter> */}
    </Card>
  );
};

export default CardList;
