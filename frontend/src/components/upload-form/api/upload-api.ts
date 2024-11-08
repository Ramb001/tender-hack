import { baseApi } from "@/shared/api";
import { UploadDtoRequest, UploadDtoResponse } from "./upload-api-dto";

export const uploadApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    uploadUrl: build.mutation<UploadDtoResponse, UploadDtoRequest>({
      query: ({ url }) => ({
        url: `/uploadUrl`,
        body: { url },
        method: "POST",
      }),
    }),
  }),
});
export const { useUploadUrlMutation } = uploadApi;