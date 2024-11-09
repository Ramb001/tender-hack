import { StatusPin } from "@/components/status-pin";
import { Checkbox } from "@/components/ui/checkbox";
import { Routes } from "@/shared/consts";
import { ColumnDef } from "@tanstack/react-table";
import { Link } from "react-router-dom";

export type Session = {
  id: string;
  status: "success" | "failed";
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
      <Link to={`${Routes.session}/${row.original.id}`}>Подробнее</Link>
    ),
  },
];
