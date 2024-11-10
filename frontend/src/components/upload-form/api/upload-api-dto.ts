import { Session } from "@/components/session-table/model/columns";

export type UploadDtoResponse = Session[];
export type UploadDtoRequest = {
  urls: string | string[];
};
