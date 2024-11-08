import { SessionList } from "@/components/session-list";
import { UploadForm } from "@/components/upload-form";

export const MainPage = () => {
  return (
    <section className="w-full flex flex-col items-center gap-10 justify-center">
      <UploadForm />
      <SessionList />
    </section>
  );
};
