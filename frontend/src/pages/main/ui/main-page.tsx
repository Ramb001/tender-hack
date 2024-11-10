import { DataTable } from "@/components/session-table";
import { columns, Session } from "@/components/session-table/model/columns";
import { MockData } from "@/components/session-table/model/mock-data";
import { UploadForm } from "@/components/upload-form";
import { useState } from "react";

export const MainPage = () => {
  const [data, setData] = useState<Session[] | null>(null);

  return (
    <section className="w-full flex flex-col items-center gap-10 justify-center">
      <UploadForm setData={setData} />
      <DataTable columns={columns} data={data || MockData} />
    </section>
  );
};
