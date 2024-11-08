import { cn } from "@/lib/utils";
type StatusPinProps = {
  status?: unknown;
};
export const StatusPin = (props: StatusPinProps) => {
  const { status } = props;
  return (
    <div className="flex items-center gap-4">
      <p>заключен</p>
      <div className={cn("rounded-full size-3 bg-main-red")} />
    </div>
  );
};
