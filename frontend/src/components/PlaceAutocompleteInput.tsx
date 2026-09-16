'use client';

import React, { useEffect, useRef } from 'react';
import { useMapsLibrary } from '@vis.gl/react-google-maps';

interface PlaceResult {
  name: string;
  formatted_address?: string;
  lat?: number;
  lng?: number;
  place_id?: string;
}

interface PlaceAutocompleteInputProps {
  id: string;
  label: string;
  placeholder: string;
  value: string;
  icon: string;
  onChangeText: (text: string) => void;
  onSelectPlace: (place: PlaceResult) => void;
  required?: boolean;
}

export default function PlaceAutocompleteInput({
  id,
  label,
  placeholder,
  value,
  icon,
  onChangeText,
  onSelectPlace,
  required = false,
}: PlaceAutocompleteInputProps) {
  const placesLibrary = useMapsLibrary('places');
  const autocompleteRef = useRef<google.maps.places.PlaceAutocompleteElement | null>(null);

  useEffect(() => {
    if (!placesLibrary || !autocompleteRef.current) {
      return;
    }

    const element = autocompleteRef.current as HTMLElement & {
      value?: string;
      addEventListener: (type: string, listener: EventListener) => void;
      removeEventListener: (type: string, listener: EventListener) => void;
    };
    const handleInput = () => onChangeText(element.value || '');
    const handleSelect = async (event: Event) => {
      const placePrediction = (event as CustomEvent<{ placePrediction?: google.maps.places.PlacePrediction }>).detail?.placePrediction;
      if (!placePrediction) return;

      const place = placePrediction.toPlace();
      await place.fetchFields({ fields: ['id', 'displayName', 'formattedAddress', 'location'] });
      const location = place.location;
      const displayName = place.displayName || place.formattedAddress || '';
      element.value = displayName;
      onSelectPlace({
        name: displayName,
        formatted_address: place.formattedAddress || undefined,
        lat: location?.lat(),
        lng: location?.lng(),
        place_id: place.id,
      });
    };

    element.addEventListener('input', handleInput);
    element.addEventListener('gmp-select', handleSelect);
    return () => {
      element.removeEventListener('input', handleInput);
      element.removeEventListener('gmp-select', handleSelect);
    };
  }, [onChangeText, onSelectPlace, placesLibrary]);

  useEffect(() => {
    if (autocompleteRef.current && autocompleteRef.current.value !== value) {
      autocompleteRef.current.value = value;
    }
  }, [value]);

  return (
    <div className="relative w-full">
      <label htmlFor={id} className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
        {label} {required && <span className="text-emerald-500">*</span>}
      </label>

      <div className="place-autocomplete-shell relative flex items-center">
        <span className="absolute left-3.5 z-10 text-base text-slate-400 select-none">{icon}</span>
        <gmp-place-autocomplete
          ref={autocompleteRef}
          id={id}
          placeholder={placeholder}
          value={value}
          className="w-full"
        />
      </div>
    </div>
  );
}
