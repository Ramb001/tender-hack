import { baseApi } from "@/shared/api";
import { UploadDtoRequest, UploadDtoResponse } from "./upload-api-dto";

export const uploadApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    uploadUrl: build.mutation<UploadDtoResponse, UploadDtoRequest>({
      query: (body) => ({
        url: `/session/analyze`,
        body: body,
        method: "POST",
      }),
      // invalidatesTags: ["SESSION"],
    }),
  }),
});
export const { useUploadUrlMutation } = uploadApi;
