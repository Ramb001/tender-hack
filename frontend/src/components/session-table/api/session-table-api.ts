import { baseApi } from "@/shared/api";
import {
  SessionTableDtoRequst,
  SessionTableDtoResponse,
} from "./session-table-api-dto";

export const sessionTableApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    getSessionInfo: build.query<SessionTableDtoResponse, SessionTableDtoRequst>(
      {
        query: () => ({
          url: `/getSessionInfo`,

          method: "GET",
        }),
        // providesTags: ["SESSION"],
      }
    ),
  }),
});
export const { useGetSessionInfoQuery } = sessionTableApi;
