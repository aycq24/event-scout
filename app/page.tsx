"use client";

import { useEffect, useState } from "react";
import EventCard from "@/components/EventCard";

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

export default function Home() {
  const title = "Event Scout";

  const [events, setEvents] = useState<Event[]>([]);
  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const categories = ["All", "Sports", "Concerts", "Entertainment"];

  useEffect(() => {
    async function loadEvents() {
      try {
        setLoading(true);
        setError("");

        const params = new URLSearchParams();

        if (search.trim()) {
          params.set("search", search.trim());
        }

        if (category !== "All") {
          params.set("category", category);
        }

        const queryString = params.toString();

        const url = queryString
          ? `${API_URL}/events?${queryString}`
          : `${API_URL}/events`;

        const response = await fetch(url);

        if (!response.ok) {
          throw new Error("Failed to load events.");
        }

        const data: Event[] = await response.json();
        setEvents(data);
      } catch {
        setError("Could not connect to the Event Scout backend.");
      } finally {
        setLoading(false);
      }
    }

    loadEvents();
  }, [search, category]);

  return (
    <main className="flex min-h-screen justify-center bg-gray-50">
      <div className="w-full max-w-2xl p-8">
        <h1 className="text-5xl font-bold">{title}</h1>

        <p className="mt-4 text-gray-600">
          Discover your next sports and entertainment event.
        </p>

        <div className="mt-8 flex gap-3">
          <input
            type="text"
            placeholder="Search events..."
            value={searchInput}
            onChange={(event) => setSearchInput(event.target.value)}
            className="flex-1 rounded-lg border border-gray-300 p-3"
          />

          <button
            type="button"
            onClick={() => setSearch(searchInput)}
            className="rounded-lg bg-black px-6 text-white"
          >
            Search
          </button>
        </div>

        <div className="mt-4 flex flex-wrap gap-3">
          {categories.map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => setCategory(item)}
              className={`rounded-lg px-4 py-2 ${
                category === item
                  ? "bg-black text-white"
                  : "border border-gray-300 bg-white text-gray-700"
              }`}
            >
              {item}
            </button>
          ))}
        </div>

        <section className="mt-8">
          {loading ? (
            <p className="text-gray-500">Loading events...</p>
          ) : error ? (
            <p className="text-red-600">{error}</p>
          ) : events.length === 0 ? (
            <p className="text-gray-500">No events found.</p>
          ) : (
            events.map((event) => (
              <EventCard
                key={event.id}
                id={event.id}
                title={event.title}
                city={event.city}
                category={event.category}
                date={event.date}
                venue={event.venue}
              />
            ))
          )}
        </section>
      </div>
    </main>
  );
}
