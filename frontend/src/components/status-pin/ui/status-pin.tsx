import { cn } from "@/lib/utils";
type StatusPinProps = {
  status?: boolean;
};
export const StatusPin = (props: StatusPinProps) => {
  const { status } = props;
  return (
    <div className="flex items-center gap-4">
      <p>{status ? "Успешно" : "Ошибка"}</p>
      <div
        className={cn(
          "rounded-full size-3 ",
          status ? "bg-main-green" : "bg-main-red"
        )}
      />
    </div>
  );
};
