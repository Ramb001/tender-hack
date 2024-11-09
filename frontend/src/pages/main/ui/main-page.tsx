import { SessionList } from "@/components/session-list";
import { UploadForm } from "@/components/upload-form";
import { DataTable } from '@/components/session-table';
import { columns } from '@/components/session-table/model/columns'
import { MockData } from '@/components/session-table/model/mock-data'


export const MainPage = () => {
  return (
    <section className="w-full flex flex-col items-center gap-10 justify-center">
      <UploadForm />
      <SessionList />
      <DataTable columns={columns} data={MockData}/>
    </section>
  );
};
