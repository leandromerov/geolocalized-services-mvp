"""Demo dataset: fictional service providers around Passau, Germany."""
from .services import Provider

PROVIDERS: list[Provider] = [
    Provider(1, "Donau Plumbing", "plumber", 48.5747, 13.4630, 4.8, 55),
    Provider(2, "Altstadt Rohrservice", "plumber", 48.5732, 13.4581, 4.4, 49),
    Provider(3, "Inn Electric", "electrician", 48.5680, 13.4505, 4.9, 60),
    Provider(4, "Ilz Elektrotechnik", "electrician", 48.5891, 13.4769, 4.2, 52, available=False),
    Provider(5, "Dreiflüsse Key Service", "locksmith", 48.5765, 13.4700, 4.7, 65),
    Provider(6, "Hacklberg Schlüsseldienst", "locksmith", 48.5822, 13.4498, 4.1, 58),
    Provider(7, "Sparkle Cleaning Passau", "cleaning", 48.5650, 13.4320, 4.6, 32),
    Provider(8, "Grubweg Clean Team", "cleaning", 48.5935, 13.4820, 4.3, 29),
    Provider(9, "Fix-It Handyman", "handyman", 48.5712, 13.4433, 4.5, 40),
    Provider(10, "Neustift Allround Service", "handyman", 48.5598, 13.4210, 4.0, 35),
    Provider(11, "Vilshofen Plumbing Pro", "plumber", 48.6339, 13.1866, 4.9, 50),
]
