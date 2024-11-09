import { Footer } from "@/components/footer";
import { Header } from "@/components/header";
import { Toaster } from "@/components/ui/toaster";
import { Outlet } from "react-router-dom";

export const Layout = () => {
  return (
    <div className="flex flex-col min-h-screen ">
      <Header />
      <main className="flex-grow p-10 bg-pale-blue  ">
        <Outlet />
      </main>
      <Toaster />
      <Footer />
    </div>
  );
};
