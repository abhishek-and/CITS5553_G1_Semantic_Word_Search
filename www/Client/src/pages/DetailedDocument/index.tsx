import { useRouter } from "next/router";
import { NextPageWithLayout } from "~/types/page";

const DetailedDoc: NextPageWithLayout = () => {
  const router = useRouter();
  const referenceNumber = router.query.referenceNumber;
  const query = router.query.query;
  return (
    <>
      <div>
        <h1>Reference Number:</h1>
        <p>{referenceNumber}</p>
        <h1>Query:</h1>
        <p>{query}</p>
      </div>
    </>
  );
};
export default DetailedDoc;
