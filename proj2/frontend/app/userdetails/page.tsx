import { redirect } from "next/navigation";

export default function UserDetailsPage() {
  // Route renamed: redirect old /userdetails to new /editdetails
  redirect("/editdetails");
}
