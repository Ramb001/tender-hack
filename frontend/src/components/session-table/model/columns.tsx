import { StatusPin } from "@/components/status-pin";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { cn } from "@/lib/utils";
import { Routes } from "@/shared/consts";
import { ColumnDef } from "@tanstack/react-table";
import { Link } from "react-router-dom";

export type Session = {
  id: string;
  status?: "success" | "failed";
  answers?: [
    {
      characteristic: string;
      match_percent: string;
      message: string;
    }
  ];
};

export const columns: ColumnDef<Session>[] = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")
        }
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "id",
    header: "Номер сессии",
  },
  {
    accessorKey: "status",
    header: "Статус",
    cell: ({ row }) => (
      <StatusPin status={row.original.status === "failed" ? false : true} />
    ),
  },
  {
    header: "Подробнее",
    cell: ({ row }) => (
      <Dialog>
        <DialogTrigger asChild>
          <Button variant={"secondary"}>Подробнее о выводе</Button>
        </DialogTrigger>
        <DialogContent className="min-w-[620px] flex flex-col p-4 gap-4 min-h-[420px]">
          {row.original?.answers?.map((answer) => (
            <div className="flex items-center gap-4 border rounded-xl">
              <div>{answer.characteristic}</div>
              <div
                className={cn(
                  +answer > 50 ? "text-main-green" : "text-main-red"
                )}
              >
                {answer.match_percent}
              </div>
              <div>{answer.message}</div>
            </div>
          ))}
        </DialogContent>
      </Dialog>
    ),
  },
];
