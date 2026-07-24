import Link from "next/link";
import { notFound } from "next/navigation";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type Event = {
  id: number;
  title: string;
  city: string;
  category: string;
  date: string;
  venue: string;
  description: string;
};

type EventDetailPageProps = {
  params: Promise<{
    id: string;
  }>;
};

async function getEvent(id: string): Promise<Event | null> {
  const response = await fetch(`${API_URL}/events/${id}`, {
    cache: "no-store",
  });

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error("Failed to load event.");
  }

  return response.json();
}

export default async function EventDetailPage({
  params,
}: EventDetailPageProps) {
  const { id } = await params;
  const event = await getEvent(id);

  if (!event) {
    notFound();
  }

  return (
    <main className="mx-auto max-w-2xl p-8">
      <Link href="/" className="text-blue-600">
        ← Back to events
      </Link>

      <span className="mt-8 inline-block rounded bg-blue-100 px-3 py-1 text-sm text-blue-700">
        {event.category}
      </span>

      <h1 className="mt-4 text-4xl font-bold">{event.title}</h1>

      <div className="mt-6 space-y-2 text-gray-700">
        <p>
          <strong>Date:</strong> {event.date}
        </p>

        <p>
          <strong>Venue:</strong> {event.venue}
        </p>

        <p>
          <strong>City:</strong> {event.city}
        </p>
      </div>

      <p className="mt-8 leading-7 text-gray-600">{event.description}</p>
    </main>
  );
}
