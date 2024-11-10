import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { SESSION } from "./tags";
const baseUrl = "http://localhost:8080/";
export const baseApi = createApi({
  tagTypes: [SESSION],
  reducerPath: "api",
  baseQuery: fetchBaseQuery({
    baseUrl: baseUrl,
  }),
  endpoints: () => ({}),
});
