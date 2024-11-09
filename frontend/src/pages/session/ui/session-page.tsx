import { useParams } from "react-router-dom";

export const SessionPage = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  return <section>{sessionId}</section>;
};
