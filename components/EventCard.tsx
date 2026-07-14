import Link from "next/link";

type EventCardProps = {
  id: number;
  title: string;
  city: string;
  category: string;
  date: string;
  venue: string;
};

export default function EventCard({
  id,
  title,
  city,
  category,
  date,
  venue,
}: EventCardProps) {
  return (
    <Link href={`/events/${id}`}>
      <article className="mb-4 rounded-xl border bg-white p-5 shadow-sm transition hover:shadow-lg hover:-translate-y-1">
        <span className="rounded bg-blue-100 px-2 py-1 text-sm text-blue-700">
          {category}
        </span>

        <h2 className="mt-3 text-2xl font-bold">
          {title}
        </h2>

        <div className="mt-4 space-y-1 text-gray-600">
          <p>📅 {date}</p>
          <p>📍 {venue}</p>
          <p>🌆 {city}</p>
        </div>
      </article>
    </Link>
  );
}