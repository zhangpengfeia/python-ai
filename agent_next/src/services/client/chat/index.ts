import * as ApiTest from "@/app/api/chat/route";
import { defaultHeaders, handleResolve, host } from "..";

export const path = () => host(`/chat`);

export async function getTest(body: {start_date:number, query_type: number}): Promise<ApiTest.getReturn> {
  return fetch(path(), {
    method: "POST",
    body: JSON.stringify(body),
    headers: defaultHeaders,
  }).then(handleResolve);
}
