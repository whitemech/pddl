; source: https://sites.google.com/stanford.edu/groundingpredicates
(define (domain twentybn)
	(:requirements :strips :typing :equality :negative-preconditions :quantified-preconditions :conditional-effects :domain-axioms :derived-predicates)
	(:types
		location - object
		sth - object
		void - object
	)
	(:constants
		hand - object
	)
	(:predicates
		; static properties
		(is-bendable ?a - sth)
		; TODO: Add not fluid to preconditions
		(is-fluid ?a - sth)
		(is-holdable ?a - sth)
		(is-rigid ?a - sth)
		(is-spreadable ?a - sth)
		(is-tearable ?a - sth)

		; mutable properties
		(above ?a - sth ?b - sth)
		(attached ?a - sth ?b - sth)
		(behind ?a - sth ?b - sth)
		(broken ?a - sth)
		(close ?a - sth)
		(closed ?a - sth)
		(deformed ?a - sth)
		(empty ?a - sth)
		(far ?a - sth)
		(fits ?a - sth ?b - sth)
		(folded ?a - sth)
		(full ?a - sth)
		(has-hole ?a - sth)
		(high ?a - sth)
		(in ?a - sth ?b - object)
		(infront ?a - sth ?b - sth)
		(left ?a - sth)
		(low ?a - sth)
		(nextto ?a - sth ?b - sth)
		(on ?a - sth ?b - sth)
		(onsurface ?a - sth)
		(open ?a - sth)
		(right ?a - sth)
		(stacked ?a - sth)
		(stretched ?a - sth)
		(torn ?a - sth)
		(touching ?a - object ?b - object)
		(twisted ?a - sth)
		(under ?a - sth ?b - sth)
		(upright ?a - sth)
		(visible ?a - object)
	)

	; 0 Approaching something with your camera
	(:action approach
		:parameters (?a - sth)
		:precondition (and
			(not (close ?a))
			(visible ?a)
			(not (visible hand))
		)
		:effect (close ?a)
	)

	; 1 Attaching something to something
	(:action attach
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and
			(attached ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 2 Bending something so that it deforms
	(:action bend-deform
		:parameters (?a - sth)
		:precondition (and
			(is-bendable ?a)
			(in ?a hand)
			(not (deformed ?a))
			(not (broken ?a))
			(visible ?a)
		)
		:effect (deformed ?a)
	)

	; 3 Bending something until it breaks
	(:action bend-break
		:parameters (?a - sth)
		:precondition (and
			(is-bendable ?a)
			(not (deformed ?a))
			(not (broken ?a))
			(in ?a hand)
		)
		:effect (broken ?a)
	)

	; 4 Burying something in something
	(:action bury
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (is-rigid ?b))
			(not (attached ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (in ?b hand))
			(not (in ?a ?b))
			(visible ?b)
		)
		:effect (and
			(in ?a ?b)
			(not (touching ?a hand))
			(not (visible ?a))
		)
	)

	; 5 Closing something
	(:action close
		:parameters (?a - sth)
		:precondition (and
			(not (far ?a))
			(open ?a)
			(visible ?a)
			(visible hand)
		)
		:effect (closed ?a)
	)

	; 6 Covering something with something
	(:action cover
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?a))
			(in ?b hand)
			(not (touching ?a ?b))
			(not (touching ?a hand))
			(visible ?a)
		)
		:effect (and
			(on ?b ?a)
			(not (touching ?a hand))
			(not (touching ?b hand))
			(not (visible ?a))
		)
	)

	; 7 Digging something out of something
	(:action dig
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(is-holdable ?a)
			(not (is-rigid ?b))
			(not (far ?a))
			(not (far ?b))
			(in ?a ?b)
			(not (touching ?a hand))
			(not (touching ?b hand))
			(not (visible ?a))
			(visible ?b)
			(visible hand)
		)
		:effect (and
			(visible ?a)
			(in ?a hand)
			(not (touching ?a ?b))
		)
	)

	; 8 Dropping something behind something
	(:action drop-behind
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(above ?a ?b)
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(behind ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 9 Dropping something in front of something
	(:action drop-infront
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(above ?a ?b)
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(infront ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 10 Dropping something into something
	(:action drop-into
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(above ?a ?b)
			(not (far ?b))
			(fits ?a ?b)
			(not (full ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(in ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 11 Dropping something next to something
	(:action drop-nextto
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(above ?a ?b)
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(nextto ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 12 Dropping something onto something
	(:action drop-onto
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(above ?a ?b)
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(on ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 13 Failing to put something into something because something does not fit
	(:action put-into-fail-fit
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(not (fits ?a ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 14 Folding something
	(:action fold
		:parameters (?a - sth)
		:precondition (and
			(not (is-rigid ?a))
			(not (folded ?a))
			(in ?a hand)
		)
		:effect (folded ?a)
	)

	; 15 Hitting something with something
	(:action hit
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(in ?b hand)
			(is-rigid ?b)
			(not (touching ?a ?b))
			(not (touching ?a hand))
			(visible ?a)
		)
		:effect (and)
	)

	; 16 Holding something
	(:action hold
		:parameters (?a - sth)
		:precondition (in ?a hand)
		:effect (and)
	)

	; 17 Holding something behind something
	(:action hold-behind
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(behind ?a ?b)
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 18 Holding something in front of something
	(:action hold-infront
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(infront ?a ?b)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 19 Holding something next to something
	(:action hold-nextto
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(nextto ?a ?b)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 20 Holding something over something
	(:action hold-over
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(above ?a ?b)
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 21 Laying something on the table on its side, not upright
	(:action lay-side
		:parameters (?a - sth)
		:precondition (in ?a hand)
		:effect (and
			(onsurface ?a)
			(not (touching ?a hand))
			(not (upright ?a))
		)
	)

	; 22 Letting something roll along a flat surface
	(:action let-roll
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(is-rigid ?a)
			(onsurface ?a)
			(touching ?a hand)
		)
		:effect (not (touching ?a hand))
	)

	; 23 Letting something roll down a slanted surface
	(:action roll-slanted
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(is-rigid ?a)
			(not (low ?a))
			(onsurface ?a)
			(touching ?a hand)
		)
		:effect (and
			(low ?a)
			(not (touching ?a hand))
		)
	)

	; 24 Letting something roll up a slanted surface, so it rolls back down
	(:action roll-up-down
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(is-rigid ?a)
			(not (high ?a))
			(onsurface ?a)
			(touching ?a hand)
		)
		:effect (and
			(low ?a)
			(not (touching ?a hand))
		)
	)

	; 25 Lifting a surface with something on it but not enough for it to slide down
	(:action lift-surface
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(is-rigid ?a)
			(onsurface ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (not (upright ?a))
	)

	; 26 Lifting a surface with something on it until it starts sliding down
	(:action lift-surface-sliding
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(is-rigid ?a)
			(is-rigid ?b)
			(onsurface ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (not (onsurface ?a))
	)

	; 27 Lifting something up completely without letting it drop down
	(:action lift
		:parameters (?a - sth)
		:precondition (and
			(not (high ?a))
			(in ?a hand)
			(onsurface ?a)
		)
		:effect (and
			(high ?a)
			(not (onsurface ?a))
		)
	)

	; 28 Lifting something up completely, then letting it drop down
	(:action lift-drop
		:parameters (?a - sth)
		:precondition (and
			(not (high ?a))
			(in ?a hand)
			(onsurface ?a)
		)
		:effect (and
			(low ?a)
			(onsurface ?a)
			(not (touching ?a hand))
		)
	)

	; 29 Lifting something with something on it
	(:action lift-with
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(is-holdable ?b)
			(is-rigid ?a)
			(is-rigid ?b)
			(not (attached ?a ?b))
			(not (far ?b))
			(not (high ?a))
			(not (high ?b))
			(in ?a hand)
			(not (touching ?b hand))
			(on ?b ?a)
			(onsurface ?a)
			(visible ?b)
		)
		:effect (and
			(high ?a)
			(high ?b)
			(not (onsurface ?a))
		)
	)

	; 30 Lifting up one end of something without letting it drop down
	(:action lift-end
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(is-rigid ?a)
			(onsurface ?a)
		)
		:effect (and
			(not (onsurface ?a))
			(not (upright ?a))
		)
	)

	; 31 Lifting up one end of something, then letting it drop down
	(:action lift-end-drop
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(is-rigid ?a)
			(onsurface ?a)
		)
		:effect (not (touching ?a hand))
	)

	; 32 Moving away from something with your camera
	(:action move-camera-away
		:parameters (?a - sth)
		:precondition (and
			(not (far ?a))
			(visible ?a)
			(not (visible hand))
		)
		:effect (far ?a)
	)

	; 33 Moving part of something
	(:action move-part
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(attached ?a ?b)
			(in ?a hand)
			(visible ?b)
		)
		:effect (and)
	)

	; 34 Moving something across a surface until it falls down
	(:action move-across-fall
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(not (low ?a))
			(onsurface ?a)
		)
		:effect (and
			(low ?a)
			(not (onsurface ?a))
			(not (touching ?a hand))
		)
	)

	; 35 Moving something across a surface without it falling down
	(:action move-across
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(not (low ?a))
			(onsurface ?a)
		)
		:effect (and)
	)

	; 36 Moving something and something away from each other
	(:action move-away
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (attached ?a ?b))
			(in ?a hand)
			(in ?b hand)
			(nextto ?a ?b)
		)
		:effect (and
			(not (nextto ?a ?b))
			(not (touching ?a ?b))
		)
	)

	; 37 Moving something and something closer to each other
	(:action move-closer
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(in ?a hand)
			(in ?b hand)
			(not (above ?a ?b))
			(not (behind ?a ?b))
			(not (infront ?a ?b))
			(not (nextto ?a ?b))
			(not (touching ?a ?b))
			(not (under ?a ?b))
		)
		:effect (nextto ?a ?b)
	)

	; 38 Moving something and something so they collide with each other
	(:action move-collide
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(in ?a hand)
			(in ?b hand)
			(not (above ?a ?b))
			(not (behind ?a ?b))
			(not (infront ?a ?b))
			(not (nextto ?a ?b))
			(not (touching ?a ?b))
			(not (under ?a ?b))
		)
		:effect (and
			(nextto ?a ?b)
			(touching ?a ?b)
		)
	)

	; 39 Moving something and something so they pass each other
	(:action move-pass
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(in ?a hand)
			(in ?b hand)
			(not (above ?a ?b))
			(not (behind ?a ?b))
			(not (infront ?a ?b))
			(not (nextto ?a ?b))
			(not (touching ?a ?b))
			(not (under ?a ?b))
		)
		:effect (and)
	)

	; 40 Moving something away from something
	(:action move-one-away
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (attached ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(nextto ?a ?b)
			(visible ?b)
		)
		:effect (and
			(not (nextto ?a ?b))
			(not (touching ?a ?b))
		)
	)

	; 41 Moving something away from the camera
	(:action move-away-from
		:parameters (?a - sth)
		:precondition (and
			(close ?a)
			(in ?a hand)
		)
		:effect (not (close ?a))
	)

	; 42 Moving something closer to something
	(:action move-closer-to
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (nextto ?a ?b))
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (nextto ?a ?b)
	)

	; 43 Moving something down
	(:action move-down
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(not (low ?a))
		)
		:effect (low ?a)
	)

	; 44 Moving something towards the camera
	(:action move-towards
		:parameters (?a - sth)
		:precondition (and
			(not (close ?a))
			(in ?a hand)
		)
		:effect (close ?a)
	)

	; 45 Moving something up
	(:action move-up
		:parameters (?a - sth)
		:precondition (and
			(not (high ?a))
			(in ?a hand)
		)
		:effect (high ?a)
	)

	; 46 Opening something
	(:action open
		:parameters (?a - sth)
		:precondition (and
			(closed ?a)
			(not (far ?a))
			(visible ?a)
			(visible hand)
		)
		:effect (open ?a)
	)

	; 47 Picking something up
	(:action pick
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(not (far ?a))
			(onsurface ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (and
			(in ?a hand)
			(not (onsurface ?a))
		)
	)

	; 48 Piling something up
	; Inconsistent definition of "piling"
	(:action pile
		:parameters (?void - void)
		:precondition (and)
		:effect (and)
	)

	; 49 Plugging something into something
	(:action plug
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(fits ?a ?b)
			(in ?a hand)
			(is-rigid ?b)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(attached ?a ?b)
			(in ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 50 Plugging something into something but pulling it right out as you remove your hand
	(:action plug-pull
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(fits ?a ?b)
			(in ?a hand)
			(is-rigid ?b)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 51 Poking a hole into some substance
	(:action poke-hole-substance
		:parameters (?a - sth)
		:precondition (and
			(is-fluid ?a)
			(not (far ?a))
			(not (has-hole ?a))
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (has-hole ?a)
	)

	; 52 Poking a hole into something soft
	(:action poke-hole-soft
		:parameters (?a - sth)
		:precondition (and
			(not (is-fluid ?a))
			(not (is-rigid ?a))
			(not (far ?a))
			(not (has-hole ?a))
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (has-hole ?a)
	)

	; 53 Poking a stack of something so the stack collapses
	(:action poke-stack-collapse
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(not (far ?a))
			(onsurface ?a)
			(stacked ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (not (stacked ?a))
	)

	; 54 Poking a stack of something without the stack collapsing
	(:action poke-stack
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(not (far ?a))
			(onsurface ?a)
			(stacked ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 55 Poking something so it slightly moves
	(:action poke-move
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(not (far ?a))
			(onsurface ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 56 Poking something so lightly that it doesn't or almost doesn't move
	(:action poke
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(not (far ?a))
			(onsurface ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 57 Poking something so that it falls over
	(:action poke-fall
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(not (far ?a))
			(onsurface ?a)
			(upright ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (not (upright ?a))
	)

	; 58 Poking something so that it spins around
	(:action poke-spin
		:parameters (?a - sth)
		:precondition (and
			(not (far ?a))
			(is-holdable ?a)
			(is-rigid ?a)
			(onsurface ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 59 Pouring something into something
	(:action pour-into
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(above ?a ?b)
			(not (full ?b))
			(in ?a hand)
			(is-fluid ?a)
			(is-rigid ?b)
			(visible ?b)
		)
		:effect (and
			(not (empty ?b))
			(in ?a ?b)
		)
	)

	; 60 Pouring something into something until it overflows
	(:action pour-into-overflow
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(in ?a hand)
			(is-fluid ?a)
			(is-rigid ?b)
			(above ?a ?b)
			(not (full ?b))
			(visible ?b)
		)
		:effect (and
			(full ?b)
			(in ?a ?b)
			(visible ?a)
		)
	)

	; 61 Pouring something onto something
	(:action pour-onto
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(in ?a hand)
			(is-fluid ?a)
			(above ?a ?b)
			(visible ?b)
		)
		:effect (and
			(on ?a ?b)
			(visible ?a)
		)
	)

	; 62 Pouring something out of something
	(:action pour-out
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (empty ?b))
			(is-fluid ?a)
			(is-rigid ?b)
			(in ?a ?b)
			(in ?b hand)
		)
		:effect (and
			(not (full ?b))
			(under ?a ?b)
			(visible ?a)
		)
	)

	; 63 Pretending or failing to wipe something off of something
	(:action wipe-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?a))
			(not (far ?b))
			(is-rigid ?b)
			(on ?a ?b)
			(visible ?a)
			(visible ?b)
			(visible hand)
		)
		:effect (and)
	)

	; 64 Pretending or trying and failing to twist something
	(:action twist-fail
		:parameters (?a - sth)
		:precondition (and
			(not (broken ?a))
			(in ?a hand)
			(not (twisted ?a))
			(not (deformed ?a))
			(visible hand)
		)
		:effect (and)
	)

	; 65 Pretending to be tearing something that is not tearable
	(:action tear-fail
		:parameters (?a - sth)
		:precondition (and
			(not (is-tearable ?a))
			(in ?a hand)
		)
		:effect (and)
	)

	; 66 Pretending to close something without actually closing it
	(:action close-fail
		:parameters (?a - sth)
		:precondition (and
			(not (far ?a))
			(open ?a)
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 67 Pretending to open something without actually opening it
	(:action open-fail
		:parameters (?a - sth)
		:precondition (and
			(closed ?a)
			(not (far ?a))
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 68 Pretending to pick something up
	(:action pick-fail
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(not (far ?a))
			(onsurface ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 69 Pretending to poke something
	(:action poke-fail
		:parameters (?a - sth)
		:precondition (and
			(not (far ?a))
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 70 Pretending to pour something out of something, but something is empty
	(:action pour-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(empty ?b)
			(in ?b hand)
			(not (in ?a ?b))
			(is-rigid ?b)
			(not (visible ?a))
		)
		:effect (and)
	)

	; 71 Pretending to put something behind something
	(:action put-behind-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(not (behind ?a ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 72 Pretending to put something into something
	(:action put-into-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 73 Pretending to put something next to something
	(:action put-nextto-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(in ?a hand)
			(not (above ?a ?b))
			(not (behind ?a ?b))
			(not (far ?b))
			(not (infront ?a ?b))
			(not (nextto ?a ?b))
			(not (touching ?a ?b))
			(not (under ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 74 Pretending to put something on a surface
	(:action put-onsurface-fail
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(not (onsurface ?a))
		)
		:effect (and)
	)

	; 75 Pretending to put something onto something
	(:action put-onto-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 76 Pretending to put something underneath something
	(:action put-under-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(not (under ?b ?a))
			(visible ?b)
		)
		:effect (and)
	)

	; 77 Pretending to scoop something up with something
	(:action scoop-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?a))
			(in ?b hand)
			(is-fluid ?a)
			(is-rigid ?b)
			(not (touching ?a ?b))
			(not (touching ?a hand))
			(visible ?a)
		)
		:effect (and)
	)

	; 78 Pretending to spread air onto something
	(:action spread-fail
		:parameters (?a - sth)
		:precondition (and
			(not (far ?a))
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 79 Pretending to sprinkle air onto something
	(:action sprinkle-fail
		:parameters (?a - sth)
		:precondition (and
			(not (far ?a))
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 80 Pretending to squeeze something
	(:action squeeze-fail
		:parameters (?a - sth)
		:precondition (and
			(not (deformed ?a))
			(in ?a hand)
		)
		:effect (and)
	)

	; 81 Pretending to take something from somewhere
	(:action take-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(not (touching ?a hand))
			(on ?a ?b)
			(visible ?a)
			(visible ?b)
			(visible hand)
		)
		:effect (and)
	)

	; 82 Pretending to take something out of something
	(:action take-out-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(fits ?a ?b)
			(in ?a ?b)
			(not (touching ?a hand))
			(not (touching ?b hand))
			(visible ?a)
			(visible ?b)
			(visible hand)
		)
		:effect (and)
	)

	; 83 Pretending to throw something
	(:action throw-fail
		:parameters (?a - sth)
		:precondition (in ?a hand)
		:effect (and)
	)

	; 84 Pretending to turn something upside down
	(:action turn-fail
		:parameters (?a - sth)
		:precondition (and
			(not (far ?a))
			(onsurface ?a)
			(not (touching ?a hand))
			(upright ?a)
			(visible ?a)
			(visible hand)
		)
		:effect (and)
	)

	; 85 Pulling something from behind of something
	(:action pull-behind
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(behind ?a ?b)
			(not (far ?a))
			(not (far ?b))
			(is-holdable ?a)
			(not (touching ?a hand))
			(visible ?b)
			(visible hand)
		)
		:effect (and
			(not (behind ?a ?b))
			(in ?a hand)
		)
	)

	; 86 Pulling something from left to right
	(:action pull-right
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(left ?a)
		)
		:effect (right ?a)
	)

	; 87 Pulling something from right to left
	(:action pull-left
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(right ?a)
		)
		:effect (left ?a)
	)

	; 88 Pulling something onto something
	(:action pull-onto
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (on ?a ?b)
	)

	; 89 Pulling something out of something
	(:action pull-out
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(fits ?a ?b)
			(in ?a hand)
			(in ?a ?b)
			(visible ?b)
		)
		:effect (not (touching ?a ?b))
	)

	; 90 Pulling two ends of something but nothing happens
	(:action pull-ends
		:parameters (?a - sth)
		:precondition (and
			(not (broken ?a))
			(in ?a hand)
			(is-rigid ?a)
			(not (stretched ?a))
		)
		:effect (and)
	)

	; 91 Pulling two ends of something so that it gets stretched
	(:action pull-stretch
		:parameters (?a - sth)
		:precondition (and
			(not (broken ?a))
			(in ?a hand)
			(not (is-rigid ?a))
			(not (stretched ?a))
		)
		:effect (stretched ?a)
	)

	; 92 Pulling two ends of something so that it separates into two pieces
	(:action pull-break
		:parameters (?a - sth)
		:precondition (and
			(not (broken ?a))
			(in ?a hand)
			(not (stretched ?a))
		)
		:effect (broken ?a)
	)

	; 93 Pushing something from left to right
	(:action push-right
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(left ?a)
			(onsurface ?a)
			(touching ?a hand)
		)
		:effect (right ?a)
	)

	; 94 Pushing something from right to left
	(:action push-left
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(right ?a)
			(onsurface ?a)
			(touching ?a hand)
		)
		:effect (left ?a)
	)

	; 95 Pushing something off of something
	(:action push-off
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (attached ?a ?b))
			(is-holdable ?a)
			(on ?a ?b)
			(touching ?a hand)
			(visible ?b)
		)
		:effect (and
			(not (above ?a ?b))
			(not (touching ?a ?b))
			(not (touching ?a hand))
			(not (touching ?b hand))
		)
	)

	; 96 Pushing something onto something
	(:action push-onto
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(is-holdable ?a)
			(touching ?a hand)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and
			(on ?a ?b)
			(not (touching ?a hand))
			(not (touching ?b hand))
		)
	)

	; 97 Pushing something so it spins
	(:action push-spin
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(is-rigid ?a)
			(onsurface ?a)
			(in ?a hand)
		)
		:effect (not (touching ?a hand))
	)

	; 98 Pushing something so that it almost falls off but doesn't
	(:action push-edge
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(onsurface ?a)
			(touching ?a hand)
			(visible ?a)
		)
		:effect (not (touching ?a hand))
	)

	; 99 Pushing something so that it falls off the table
	(:action push-fall
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(onsurface ?a)
			(touching ?a hand)
			(visible ?a)
		)
		:effect (far ?a)
	)

	; 100 Pushing something so that it slightly moves
	(:action push
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(onsurface ?a)
			(touching ?a hand)
			(visible ?a)
		)
		:effect (and)
	)

	; 101 Pushing something with something
	(:action push-with
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(is-holdable ?b)
			(in ?b hand)
			(is-rigid ?b)
			(onsurface ?a)
			(not (touching ?a ?b))
			(not (touching ?a hand))
			(visible ?a)
		)
		:effect (touching ?a ?b)
	)

	; 102 Putting number of something onto something
	; Unable to handle [number of] placeholder.
	(:action put-many-onto
		:parameters (?void - void)
		:precondition (and)
		:effect (and)
	)

	; 103 Putting something and something on the table
	(:action put-two
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(in ?a hand)
			(is-holdable ?b)
			(not (attached ?a ?b))
			(not (onsurface ?a))
			(not (onsurface ?b))
			(not (touching ?a ?b))
			(not (visible ?b))
		)
		:effect (and
			(onsurface ?a)
			(onsurface ?b)
			(not (touching ?a hand))
			(not (touching ?b hand))
			(visible ?b)
		)
	)

	; 104 Putting something behind something
	(:action put-behind
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (behind ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(behind ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 105 Putting something in front of something
	(:action put-infront
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (infront ?a ?b))
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(infront ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 106 Putting something into something
	(:action put-into
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(fits ?a ?b)
			(not (full ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(in ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 107 Putting something next to something
	(:action put-nextto
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(not (nextto ?a ?b))
			(onsurface ?b)
			(not (onsurface ?a))
			(in ?a hand)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(nextto ?a ?b)
			(onsurface ?a)
			(not (touching ?a hand))
		)
	)

	; 108 Putting something on a flat surface without letting it roll
	(:action put-onsurface-noroll
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(is-rigid ?a)
			(not (onsurface ?a))
		)
		:effect (and
			(onsurface ?a)
			(not (touching ?a hand))
		)
	)

	; 109 Putting something on a surface
	(:action put-onsurface
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(not (onsurface ?a))
		)
		:effect (and
			(onsurface ?a)
			(not (touching ?a hand))
		)
	)

	; 110 Putting something on the edge of something so it is not supported and falls down
	(:action put-edge-fall
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(is-rigid ?a)
			(not (low ?a))
			(onsurface ?b)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(low ?a)
			(onsurface ?a)
			(not (touching ?a hand))
		)
	)

	; 111 Putting something onto a slanted surface but it doesn't glide down
	(:action put-slanted
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(is-rigid ?a)
			(not (onsurface ?a))
		)
		:effect (and
			(onsurface ?a)
			(not (touching ?a hand))
			(not (upright ?a))
		)
	)

	; 112 Putting something onto something
	(:action put-onto
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(onsurface ?b)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(on ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 113 Putting something onto something else that cannot support it so it falls down
	(:action put-fall
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(is-rigid ?b)
			(not (low ?a))
			(onsurface ?b)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(low ?a)
			(onsurface ?a)
			(not (touching ?a hand))
			(not (upright ?a))
		)
	)

	; 114 Putting something similar to other things that are already on the table
	(:action put-similar
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(not (onsurface ?a))
		)
		:effect (and
			(not (touching ?a hand))
			(onsurface ?a)
		)
	)

	; 115 Putting something that can't roll onto a slanted surface, so it slides down
	(:action put-slide
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(is-rigid ?a)
			(not (onsurface ?a))
			(not (upright ?a))
		)
		:effect (and
			(low ?a)
			(onsurface ?a)
			(not (touching ?a hand))
		)
	)

	; 116 Putting something that can't roll onto a slanted surface, so it stays where it is
	(:action put-slanted-noslide
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(is-rigid ?a)
			(not (onsurface ?a))
			(not (upright ?a))
		)
		:effect (and
			(onsurface ?a)
			(not (low ?a))
			(not (touching ?a hand))
		)
	)

	; 117 Putting something that cannot actually stand upright upright on the table, so it falls on its side
	(:action put-side
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(is-rigid ?a)
			(not (onsurface ?a))
		)
		:effect (and
			(onsurface ?a)
			(not (touching ?a hand))
			(not (upright ?a))
		)
	)

	; 118 Putting something underneath something
	(:action put-under
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(not (under ?a ?b))
			(visible ?b)
		)
		:effect (and
			(not (touching ?a hand))
			(under ?a ?b)
		)
	)

	; 119 Putting something upright on the table
	(:action put-upright
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(is-rigid ?a)
			(not (onsurface ?a))
		)
		:effect (and
			(onsurface ?a)
			(not (touching ?a hand))
			(upright ?a)
		)
	)

	; 120 Putting something, something and something on the table
	(:action put-three
		:parameters (?a - sth ?b - sth ?c - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (= ?a ?c))
			(not (= ?b ?c))
			(is-holdable ?b)
			(is-holdable ?c)
			(not (attached ?a ?b))
			(not (attached ?a ?c))
			(not (attached ?b ?c))
			(in ?a hand)
			(not (onsurface ?a))
			(not (onsurface ?b))
			(not (onsurface ?c))
			(not (touching ?b hand))
			(not (touching ?c hand))
			(not (touching ?a ?b))
			(not (touching ?a ?c))
			(not (touching ?b ?c))
			(not (visible ?b))
			(not (visible ?c))
		)
		:effect (and
			(onsurface ?a)
			(onsurface ?b)
			(onsurface ?c)
			(not (touching ?a hand))
			(visible ?b)
			(visible ?c)
		)
	)

	; 121 Removing something, revealing something behind
	(:action remove-reveal
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(behind ?b ?a)
			(in ?a hand)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(not (visible ?b))
		)
		:effect (and
			(not (behind ?b ?a))
			(visible ?b)
		)
	)

	; 122 Rolling something on a flat surface
	(:action roll
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(is-rigid ?a)
			(onsurface ?a)
			(not (upright ?a))
		)
		:effect (not (touching ?a hand))
	)

	; 123 Scooping something up with something
	(:action scoop
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?a))
			(in ?b hand)
			(is-fluid ?a)
			(is-rigid ?b)
			(not (touching ?a ?b))
			(not (touching ?a hand))
			(visible ?a)
		)
		:effect (in ?a ?b)
	)

	; 124 Showing a photo of something to the camera
	(:action show-photo
		:parameters (?a - sth)
		:precondition (and
			(close ?a)
			(visible ?a)
		)
		:effect (and)
	)

	; 125 Showing something behind something
	(:action show-behind
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(behind ?a ?b)
			(close ?a)
			(close ?b)
			(visible ?a)
			(visible ?b)
		)
		:effect (and)
	)

	; 126 Showing something next to something
	(:action show-nextto
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(close ?a)
			(close ?b)
			(nextto ?a ?b)
			(not (touching ?a ?b))
			(visible ?a)
			(visible ?b)
		)
		:effect (and)
	)

	; 127 Showing something on top of something
	(:action show-on
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (attached ?a ?b))
			(close ?a)
			(close ?b)
			(on ?a ?b)
			(visible ?a)
			(visible ?b)
		)
		:effect (and)
	)

	; 128 Showing something to the camera
	(:action show
		:parameters (?a - sth)
		:precondition (and
			(close ?a)
			(visible ?a)
		)
		:effect (and)
	)

	; 129 Showing that something is empty
	(:action show-empty
		:parameters (?a - sth)
		:precondition (and
			(close ?a)
			(visible ?a)
		)
		:effect (empty ?a)
	)

	; 130 Showing that something is inside something
	(:action show-in
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(close ?a)
			(close ?b)
			(in ?a ?b)
			(visible ?a)
			(visible ?b)
		)
		:effect (and)
	)

	; 131 Something being deflected from something
	(:action deflect
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(is-holdable ?a)
			(is-holdable ?b)
			(is-rigid ?a)
			(is-rigid ?b)
			(not (touching ?a ?b))
			(visible ?a)
			(visible ?b)
		)
		:effect (and)
	)

	; 132 Something colliding with something and both are being deflected
	(:action collide-deflect
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(is-holdable ?a)
			(is-holdable ?b)
			(is-rigid ?a)
			(is-rigid ?b)
			(not (touching ?a ?b))
			(visible ?a)
			(visible ?b)
		)
		:effect (and)
	)

	; 133 Something colliding with something and both come to a halt
	(:action collide-halt
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(is-holdable ?a)
			(is-holdable ?b)
			(is-rigid ?a)
			(is-rigid ?b)
			(not (touching ?a ?b))
			(visible ?a)
			(visible ?b)
		)
		:effect (nextto ?a ?b)
	)

	; 134 Something falling like a feather or paper
	(:action drop-light
		:parameters (?a - sth)
		:precondition (and
			(not (low ?a))
			(not (is-rigid ?a))
			(in ?a hand)
		)
		:effect (and
			(low ?a)
			(not (touching ?a hand))
		)
	)

	; 135 Something falling like a rock
	(:action drop-heavy
		:parameters (?a - sth)
		:precondition (and
			(not (low ?a))
			(in ?a hand)
			(is-rigid ?a)
		)
		:effect (and
			(low ?a)
			(not (touching ?a hand))
		)
	)

	; 136 Spilling something behind something
	(:action spill-behind
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (behind ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(is-fluid ?a)
			(onsurface ?b)
			(not (onsurface ?a))
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and
			(behind ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 137 Spilling something next to something
	(:action spill-nextto
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(is-fluid ?a)
			(not (nextto ?a ?b))
			(onsurface ?b)
			(not (onsurface ?a))
			(not (touching ?a ?b))
			(visible ?a)
		)
		:effect (and
			(nextto ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 138 Spilling something onto something
	(:action spill-on
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(is-fluid ?a)
			(onsurface ?b)
			(not (onsurface ?a))
			(not (touching ?a ?b))
			(visible ?a)
			(not (= ?a ?b))
			(is-fluid ?a)
		)
		:effect (and
			(on ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 139 Spinning something so it continues spinning
	(:action spin-long
		:parameters (?a - sth)
		:precondition (and
			(onsurface ?a)
			(in ?a hand)
			(is-rigid ?a)
			(not (upright ?a))
		)
		:effect (not (touching ?a hand))
	)

	; 140 Spinning something that quickly stops spinning
	(:action spin-short
		:parameters (?a - sth)
		:precondition (and
			(onsurface ?a)
			(in ?a hand)
			(not (upright ?a))
		)
		:effect (not (touching ?a hand))
	)

	; 141 Spreading something onto something
	(:action spread
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(is-spreadable ?a)
			(not (far ?b))
			(in ?a hand)
			(visible ?b)
		)
		:effect (and
			(on ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 142 Sprinkling something onto something
	(:action sprinkle
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(above ?a ?b)
			(in ?a hand)
			(is-fluid ?a)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(on ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 143 Squeezing something
	(:action squeeze
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(not (is-rigid ?a))
			(not (deformed ?a))
		)
		:effect (and)
	)

	; 144 Stacking number of something
	; Unable to handle [number of] placeholder.
	(:action stack
		:parameters (?void - void)
		:precondition (and)
		:effect (and)
	)

	; 145 Stuffing something into something
	(:action stuff
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?b))
			(fits ?a ?b)
			(not (full ?b))
			(in ?a hand)
			(not (is-rigid ?a))
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (and
			(in ?a ?b)
			(not (touching ?a hand))
		)
	)

	; 146 Taking one of many similar things on the table
	(:action take-one
		:parameters (?a - sth)
		:precondition (and
			(not (far ?a))
			(onsurface ?a)
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (in ?a hand)
	)

	; 147 Taking something from somewhere
	(:action take-from
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?a))
			(not (far ?b))
			(on ?a ?b)
			(not (touching ?a hand))
			(visible ?a)
			(visible ?b)
			(visible hand)
		)
		:effect (and
			(in ?a hand)
			(not (touching ?a ?b))
		)
	)

	; 148 Taking something out of something
	(:action take-out
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?a))
			(not (far ?b))
			(fits ?a ?b)
			(in ?a ?b)
			(not (touching ?a hand))
			(visible ?b)
			(visible hand)
		)
		:effect (and
			(in ?a hand)
			(not (touching ?a ?b))
			(visible ?a)
		)
	)

	; 149 Tearing something into two pieces
	(:action tear-pieces
		:parameters (?a - sth)
		:precondition (and
			(is-tearable ?a)
			(in ?a hand)
			(not (torn ?a))
			(not (broken ?a))
		)
		:effect (and
			(broken ?a)
			(torn ?a)
		)
	)

	; 150 Tearing something just a little bit
	(:action tear
		:parameters (?a - sth)
		:precondition (and
			(is-tearable ?a)
			(in ?a hand)
			(not (broken ?a))
			(not (torn ?a))
		)
		:effect (torn ?a)
	)

	; 151 Throwing something
	(:action throw
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(not (onsurface ?a))
		)
		:effect (and
			(far ?a)
			(not (touching ?a hand))
			(onsurface ?a)
		)
	)

	; 152 Throwing something against something
	(:action throw-against
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(in ?a hand)
			(not (onsurface ?a))
			(onsurface ?b)
			(not (touching ?a ?b))
			(not (touching ?b hand))
			(visible ?b)
		)
		:effect (not (touching ?a hand))
	)

	; 153 Throwing something in the air and catching it
	(:action throw-catch
		:parameters (?a - sth)
		:precondition (in ?a hand)
		:effect (and)
	)

	; 154 Throwing something in the air and letting it fall
	(:action throw-fall
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(not (onsurface ?a))
		)
		:effect (not (touching ?a hand))
	)

	; 155 Throwing something onto a surface
	(:action throw-surface
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(not (onsurface ?a))
		)
		:effect (and
			(far ?a)
			(onsurface ?a)
			(not (touching ?a hand))
		)
	)

	; 156 Tilting something with something on it slightly so it doesn't fall down
	(:action tilt
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (attached ?a ?b))
			(in ?a hand)
			(is-holdable ?b)
			(is-rigid ?a)
			(is-rigid ?b)
			(on ?b ?a)
			(visible ?b)
		)
		:effect (and)
	)

	; 157 Tilting something with something on it until it falls off
	(:action tilt-fall
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(is-holdable ?b)
			(not (attached ?a ?b))
			(in ?a hand)
			(is-rigid ?a)
			(is-rigid ?b)
			(on ?b ?a)
			(visible ?b)
		)
		:effect (and
			(not (touching ?a ?b))
			(not (upright ?a))
		)
	)

	; 158 Tipping something over
	(:action tip
		:parameters (?a - sth)
		:precondition (and
			(is-holdable ?a)
			(is-rigid ?a)
			(onsurface ?a)
			(touching ?a hand)
			(upright ?a)
		)
		:effect (and
			(not (touching ?a hand))
			(not (upright ?a))
		)
	)

	; 159 Tipping something with something in it over, so something in it falls out
	(:action tip-fall-out
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (attached ?a ?b))
			(fits ?b ?a)
			(in ?b ?a)
			(is-holdable ?a)
			(is-rigid ?a)
			(not (onsurface ?b))
			(touching ?a hand)
			(not (touching ?b hand))
			(upright ?a)
		)
		:effect (and
			(not (in ?b ?a))
			(not (touching ?a hand))
			(not (upright ?a))
			(onsurface ?b)
			(visible ?b)
		)
	)

	; 160 Touching (without moving) part of something
	(:action touch
		:parameters (?a - sth)
		:precondition (and
			(not (far ?a))
			(not (touching ?a hand))
			(visible ?a)
			(visible hand)
		)
		:effect (touching ?a hand)
	)

	; 161 Trying but failing to attach something to something because it doesn't stick
	(:action attach-fail
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (attached ?a ?b))
			(not (far ?b))
			(in ?a hand)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (and)
	)

	; 162 Trying to bend something unbendable so nothing happens
	(:action bend-fail
		:parameters (?a - sth)
		:precondition (and
			(not (broken ?a))
			(not (is-bendable ?a))
			(is-rigid ?a)
			(in ?a hand)
		)
		:effect (and)
	)

	; 163 Trying to pour something into something, but missing so it spills next to it
	(:action pour-miss
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(above ?a ?b)
			(in ?a hand)
			(is-fluid ?a)
			(is-rigid ?b)
			(not (touching ?a ?b))
			(visible ?b)
		)
		:effect (nextto ?a ?b)
	)

	; 164 Turning something upside down
	(:action turn-upsidedown
		:parameters (?a - sth)
		:precondition (and
			(in ?a hand)
			(is-rigid ?a)
			(upright ?a)
		)
		:effect (not (upright ?a))
	)

	; 165 Turning the camera downwards while filming something
	(:action turn-camera-down
		:parameters (?a - sth)
		:precondition (and
			(not (high ?a))
			(visible ?a)
			(not (visible hand))
		)
		:effect (high ?a)
	)

	; 166 Turning the camera left while filming something
	(:action turn-camera-left
		:parameters (?a - sth)
		:precondition (and
			(not (right ?a))
			(visible ?a)
			(not (visible hand))
		)
		:effect (right ?a)
	)

	; 167 Turning the camera right while filming something
	(:action turn-camera-right
		:parameters (?a - sth)
		:precondition (and
			(not (left ?a))
			(visible ?a)
			(not (visible hand))
		)
		:effect (left ?a)
	)

	; 168 Turning the camera upwards while filming something
	(:action turn-camera-up
		:parameters (?a - sth)
		:precondition (and
			(not (low ?a))
			(visible ?a)
			(not (visible hand))
		)
		:effect (low ?a)
	)

	; 169 Twisting (wringing) something wet until water comes out
	(:action twist-water
		:parameters (?a - sth)
		:precondition (and
			(not (is-rigid ?a))
			(not (broken ?a))
			(in ?a hand)
			(not (twisted ?a))
			(not (deformed ?a))
		)
		:effect (twisted ?a)
	)

	; 170 Twisting something
	(:action twist
		:parameters (?a - sth)
		:precondition (and
			(not (is-rigid ?a))
			(not (broken ?a))
			(in ?a hand)
			(not (twisted ?a))
			(not (deformed ?a))
		)
		:effect (twisted ?a)
	)

	; 171 Uncovering something
	(:action uncover
		:parameters (?a - sth)
		:precondition (and
			(not (touching ?a hand))
			(not (visible ?a))
			(visible hand)
		)
		:effect (visible ?a)
	)

	; 172 Unfolding something
	(:action unfold
		:parameters (?a - sth)
		:precondition (and
			(not (is-rigid ?a))
			(folded ?a)
			(in ?a hand)
		)
		:effect (not (folded ?a))
	)

	; 173 Wiping something off of something
	(:action wipe
		:parameters (?a - sth ?b - sth)
		:precondition (and
			(not (= ?a ?b))
			(not (far ?a))
			(not (far ?b))
			(is-rigid ?b)
			(on ?a ?b)
			(not (touching ?a hand))
			(not (touching ?b hand))
			(visible ?a)
			(visible ?b)
			(visible hand)
		)
		:effect (and
			(not (touching ?a ?b))
			(not (visible ?a))
		)
	)

	; Equal
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (= ?a ?b)
		:implies (and
			(= ?b ?a)
			(not (above ?a ?b))
			(not (attached ?a ?b))
			(not (behind ?a ?b))
			(not (fits ?a ?b))
			(not (in ?a ?b))
			(not (infront ?a ?b))
			(not (nextto ?a ?b))
			(not (on ?a ?b))
			(not (touching ?a ?b))
			(not (under ?a ?b))
		)
	)

	; Bendable
	(:axiom
		:vars (?a - sth)
		:context (not (is-bendable ?a))
		:implies (and
			(not (deformed ?a))
			(not (folded ?a))
			(not (twisted ?a))
		)
	)

	; Fluid
	(:axiom
		:vars (?a - sth)
		:context (is-fluid ?a)
		:implies (and
			(not (is-rigid ?a))
			(not (broken ?a))
			(not (closed ?a))
			(not (deformed ?a))
			(not (empty ?a))
			(not (folded ?a))
			(not (full ?a))
			(not (open ?a))
			(not (stacked ?a))
			(not (stretched ?a))
			(not (twisted ?a))
			(not (upright ?a))
			; (forall (?b - sth)
			;     (when
			;         (not (= ?a ?b))
			;         (not (attached ?a ?b))
			;     )
			; )
		)
	)

	; Holdable
	(:axiom
		:vars (?a - sth)
		:context (not (is-holdable ?a))
		:implies (not (in ?a hand))
	)

	; Rigid
	(:axiom
		:vars (?a - sth)
		:context (is-rigid ?a)
		:implies (and
			(not (is-fluid ?a))
			(not (is-spreadable ?a))
			(not (folded ?a))
			(not (stretched ?a))
			(not (torn ?a))
			(not (twisted ?a))
		)
	)

	; Spreadable
	(:axiom
		:vars (?a - sth)
		:context (is-spreadable ?a)
		:implies (and
			(not (is-rigid ?a))
			(not (broken ?a))
			(not (closed ?a))
			(not (deformed ?a))
			(not (empty ?a))
			(not (folded ?a))
			(not (full ?a))
			(not (open ?a))
			(not (stacked ?a))
			(not (stretched ?a))
			(not (twisted ?a))
			(not (upright ?a))
		)
	)

	; Tearable
	(:axiom
		:vars (?a - sth)
		:context (is-tearable ?a)
		:implies (and
			(not (deformed ?a))
			(not (stretched ?a))
		)
	)
	(:axiom
		:vars (?a - sth)
		:context (not (is-tearable ?a))
		:implies (not (torn ?a))
	)

	; Above
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (above ?a ?b)
		:implies (and
			(not (= ?a ?b))
			(not (above ?b ?a))
			(not (behind ?a ?b))
			(not (behind ?b ?a))
			(not (in ?a ?b))
			(not (in ?b ?a))
			(not (nextto ?a ?b))
			(under ?b ?a)
		)
	)
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (not (above ?a ?b))
		:implies (not (under ?b ?a))
	)

	; Attached
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (attached ?a ?b)
		:implies (and
			(not (= ?a ?b))
			(not (is-fluid ?a))
			(attached ?b ?a)
			(touching ?a ?b)
		)
	)
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (not (attached ?a ?b))
		:implies (not (attached ?b ?a))
	)

	; Behind
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (behind ?a ?b)
		:implies (and
			(not (= ?a ?b))
			(not (above ?a ?b))
			(not (above ?b ?a))
			(not (behind ?b ?a))
			(not (in ?a ?b))
			(not (in ?b ?a))
			(infront ?b ?a)
			(not (nextto ?a ?b))
		)
	)
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (not (behind ?a ?b))
		:implies (not (infront ?b ?a))
	)

	; Broken
	(:axiom
		:vars (?a - sth)
		:context (broken ?a)
		:implies (and
			(not (is-fluid ?a))
			(not (is-spreadable ?a))
		)
	)

	; Close
	(:axiom
		:vars (?a - sth)
		:context (close ?a)
		:implies (not (far ?a))
	)

	; Closed
	(:axiom
		:vars (?a - sth)
		:context (closed ?a)
		:implies (and
			(not (is-fluid ?a))
			(not (is-spreadable ?a))
			(not (open ?a))
		)
	)

	; Deformed
	(:axiom
		:vars (?a - sth)
		:context (deformed ?a)
		:implies (and
			(is-bendable ?a)
			(not (is-fluid ?a))
			(not (is-spreadable ?a))
			(not (is-tearable ?a))
		)
	)

	; Empty
	(:axiom
		:vars (?a - sth)
		:context (empty ?a)
		:implies (and
			(not (is-fluid ?a))
			(not (is-spreadable ?a))
			(not (full ?a))
		)
	)

	; Far
	(:axiom
		:vars (?a - sth)
		:context (far ?a)
		:implies (and
			(not (close ?a))
			(not (touching ?a hand))
		)
	)

	; Fits
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (fits ?a ?b)
		:implies (and
			(not (= ?a ?b))
			(not (is-fluid ?a))
			(not (is-fluid ?b))
			(not (is-spreadable ?a))
			(not (is-spreadable ?b))
		)
	)
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (not (fits ?a ?b))
		:implies (not (in ?a ?b))
	)

	; Folded
	(:axiom
		:vars (?a - sth)
		:context (folded ?a)
		:implies (and
			(is-bendable ?a)
			(not (is-fluid ?a))
			(not (is-rigid ?a))
			(not (is-spreadable ?a))
		)
	)

	; Full
	(:axiom
		:vars (?a - sth)
		:context (full ?a)
		:implies (and
			(not (is-fluid ?a))
			(not (is-spreadable ?a))
			(not (empty ?a))
		)
	)

	; High
	(:axiom
		:vars (?a - sth)
		:context (high ?a)
		:implies (not (low ?a))
	)

	; In
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (in ?a ?b)
		:implies (and
			(not (= ?a ?b))
			(not (above ?a ?b))
			(not (above ?b ?a))
			(not (behind ?a ?b))
			(not (behind ?b ?a))
			(not (empty ?b))
			(not (in ?b ?a))
			(not (on ?a ?b))
			(not (on ?b ?a))
			(touching ?a ?b)
		)
	)
	(:axiom
		:vars (?a - sth)
		:context (in ?a hand)
		:implies (and
			(is-holdable ?a)
			(not (far ?a))
			(touching ?a hand)
			(visible ?a)    ; Ensure that object and hand can be seen
			(visible hand)
		)
	)

	; In front
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (infront ?a ?b)
		:implies (and
			(not (= ?a ?b))
			(behind ?b ?a)
			(not (infront ?b ?a))
			(not (nextto ?a ?b))
		)
	)
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (not (infront ?a ?b))
		:implies (not (behind ?b ?a))
	)

	; Left
	(:axiom
		:vars (?a - sth)
		:context (left ?a)
		:implies (not (right ?a))
	)

	; Low
	(:axiom
		:vars (?a - sth)
		:context (low ?a)
		:implies (not (high ?a))
	)

	; Next to
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (nextto ?a ?b)
		:implies (and
			(not (= ?a ?b))
			(not (above ?a ?b))
			(not (behind ?a ?b))
			(not (infront ?a ?b))
			(not (under ?a ?b))
			(nextto ?b ?a)
		)
	)
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (not (nextto ?a ?b))
		:implies (and
			(not (nextto ?b ?a))
		)
	)

	; On
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (on ?a ?b)
		:implies (and
			(not (= ?a ?b))
			(above ?a ?b)
			(not (behind ?a ?b))
			(not (behind ?b ?a))
			(not (in ?a ?b))
			(not (in ?b ?a))
			(not (on ?b ?a))
			(touching ?a ?b)
		)
	)

	; Open
	(:axiom
		:vars (?a - sth)
		:context (open ?a)
		:implies (and
			(not (is-fluid ?a))
			(not (is-spreadable ?a))
			(not (closed ?a))
		)
	)

	; Right
	(:axiom
		:vars (?a - sth)
		:context (right ?a)
		:implies (not (left ?a))
	)

	; Stacked
	(:axiom
		:vars (?a - sth)
		:context (stacked ?a)
		:implies (and
			(not (is-fluid ?a))
			(not (is-spreadable ?a))
		)
	)

	; Stretched
	(:axiom
		:vars (?a - sth)
		:context (stretched ?a)
		:implies (and
			(not (is-fluid ?a))
			(not (is-rigid ?a))
			(not (is-spreadable ?a))
			(not (is-tearable ?a))
		)
	)

	; Torn
	(:axiom
		:vars (?a - sth)
		:context (torn ?a)
		:implies (is-tearable ?a)
	)

	; Touching
	(:axiom
		:vars (?a - object ?b - object)
		:context (touching ?a ?b)
		:implies (and
			(not (= ?a ?b))
			(touching ?b ?a)
		)
	)
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (not (touching ?a ?b))
		:implies (and
			(not (attached ?a ?b))
			(not (attached ?b ?a))
			(not (in ?a ?b))
			(not (in ?b ?a))
			(not (on ?a ?b))
			(not (on ?b ?a))
			(not (touching ?b ?a))
		)
	)
	(:axiom
		:vars (?a - sth)
		:context (touching ?a hand)
		:implies (and
			(not (far ?a))
			(visible ?a)    ; Ensure that object and hand can be seen
			(visible hand)
		)
	)
	(:axiom
		:vars (?a - sth)
		:context (not (touching ?a hand))
		:implies (and
			(not (in ?a hand))
			(not (touching hand ?a))
		)
	)

	; Twisted
	(:axiom
		:vars (?a - sth)
		:context (twisted ?a)
		:implies (and
			(is-bendable ?a)
			(not (is-fluid ?a))
			(not (is-rigid ?a))
			(not (is-spreadable ?a))
		)
	)

	; Under
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (under ?a ?b)
		:implies (and
			(not (= ?a ?b))
			(above ?b ?a)
			(not (under ?b ?a))
		)
	)
	(:axiom
		:vars (?a - sth ?b - sth)
		:context (not (under ?a ?b))
		:implies (not (above ?b ?a))
	)

	; Upright
	(:axiom
		:vars (?a - sth)
		:context (upright ?a)
		:implies (and
			(not (is-fluid ?a))
			(not (is-spreadable ?a))
		)
	)
)