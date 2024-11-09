import { DataTable } from "@/components/session-table";
import { columns } from "@/components/session-table/model/columns";
import { MockData } from "@/components/session-table/model/mock-data";
import { UploadForm } from "@/components/upload-form";

export const MainPage = () => {
  return (
    <section className="w-full flex flex-col items-center gap-10 justify-center">
      <UploadForm />
      <DataTable columns={columns} data={MockData} />
    </section>
  );
};
